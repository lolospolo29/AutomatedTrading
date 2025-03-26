import threading
from logging import Logger

from files.helper.builder.OrderBuilder import OrderBuilder
from files.helper.builder.RequestBuilder import RequestBuilder
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.registry.LockRegistry import LockRegistry
from files.helper.mappers.ClassMapper import ClassMapper
from files.models.asset.Relation import Relation
from files.models.broker.BrokerOrder import BrokerOrder
from files.models.broker.BrokerPosition import BrokerPosition
from files.models.broker.RequestParameters import RequestParameters
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade
from files.models.trade.enums.OrderResultStatusEnum import OrderResultStatusEnum
from files.models.trade.enums.OrderStatus import OrderStatus
from files.models.trade.enums.Side import Side


# todo service to trading service
class BrokerService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(BrokerService, cls).__new__(cls)
        return cls._instance

    def __init__(self,broker_registry:BrokerRegistry
                 , logger:Logger):
        if not hasattr(self, "_initialized"):
            self._lock_registry = LockRegistry()
            self._broker_registry = broker_registry
            self._logger = logger
            self._initialized = True

    # endregion

    #region API
    def place_order(self, requestParameters:RequestParameters) -> Order:
        newOrder: BrokerOrder = self._broker_registry.place_order(requestParameters)
        return ClassMapper.map_source_to_target_model(newOrder, Order)

    def amend_order(self, requestParameters:RequestParameters) -> Order:
        newOrder: BrokerOrder = self._broker_registry.amend_order(requestParameters)
        return ClassMapper.map_source_to_target_model(newOrder, Order)

    def cancel_order(self, requestParameters:RequestParameters) -> Order:
        newOrder: BrokerOrder = self._broker_registry.cancel_order(requestParameters)
        return ClassMapper.map_source_to_target_model(newOrder, Order)

    def set_leverage(self, request_parameters: RequestParameters) -> bool:
        return self._broker_registry.set_leverage(request_parameters)

    def cancel_all_orders(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_registry.cancel_all_orders(request_parameters)

    def get_open_and_closed_orders(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_registry.return_open_and_closed_orders(request_parameters)

    def get_position_info(self, request_parameters: RequestParameters) -> list[BrokerPosition]:
        return self._broker_registry.return_position_info(request_parameters)

    def get_order_history(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_registry.return_order_history(request_parameters)

    # endregion

    # region API Requests
    def place_trade(self, trade: Trade,relation:Relation) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        with tradeLock:
                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        request = RequestBuilder().create_request().add_order(order).add_relation(relation).build()
                        self.place_order(request)
                    except Exception as e:
                        self._logger.exception(f"Place Order Error,"
                                       f"OrderLinkId: {order.order_link_id},"
                                       f"TradeId:{order.trade_id},Symbol:{order.symbol},OrderType:{order.order_type},error:{e}")
                        exceptionOrders.append(order)
                        break

                return exceptionOrders, trade

    def amend_trade(self, order:list[Orders], relation: Relation) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        with tradeLock:
            exception_orders: list[Order] = []

            for order in trade.:
                try:
                    request = RequestBuilder().create_request().add_order(order).add_relation(relation).build()
                    if order.order_result_status == OrderResultStatusEnum.AMEND.value:
                        self.amend_order(request)
                    if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                        self.cancel_order(request)
                    if order.order_result_status == OrderResultStatusEnum.NEW.value:
                        self.place_order(request)
                except Exception as e:
                    exception_orders.append(order)
                    self._logger.exception("Amending Order Error:{e},OrderLinkId:{id},Order Status:{status},"
                                           "Symbol:{symbol}".format(e=e, id=order.orderLinkI,
                                                                    status=order.order_result_status,
                                                                    symbol=order.symbol))
        return exception_orders, trade

    def cancel_trade(self, trade: Trade,relation:Relation) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        with tradeLock:
            if trade.trade_id in self._open_trades:
                trade = self._open_trades[trade.trade_id]
                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        self.cancel_order(trade.relation_id.broker_id, order)
                    except Exception as e:
                        if order.order_status == OrderStatus.NEW.value or order.order_status == OrderStatus.PARTIALLYFILLED.value or order.order_status == OrderStatus.UNTRIGGERED.value:
                            exceptionOrders.append(order)
                            self._logger.error(f"Failed To Cancel Order,Error:{e},OrderLinkId: "
                                         f"{order.order_link_id},TradeId:{order.trade_id},Symbol:{order.symbol},OrderType:{order.order_type}")

                cancel_size_order = OrderBuilder().create_order(relation=trade.relation_id, entry_frame_work=None
                                                                , symbol=trade.relation_id.asset, confirmations=[]
                                                                , category=trade.category, side=trade.side
                                                                , risk_percentage=0, order_number=1
                                                                , tradeId=trade.trade_id).set_defaults(
                                                                  reduce_only=True).build()
                if trade.side == Side.BUY.value:
                    cancel_size_order.side = Side.SELL.value
                if trade.side == Side.SELL.value:
                    cancel_size_order.side = Side.BUY.value
                cancel_size_order.qty = trade.size

                try:
                    if int(cancel_size_order.qty) > 0:
                        trade.orders.append(cancel_size_order)
                        cancel_size_order = self.place_order(trade.relation_id.broker_id, cancel_size_order)
                    else:
                        self._logger.info("Cancel Order Failed due to 0 Qty,OrderLinkId:{id}".format(id=cancel_size_order.trade_id, ))
                except Exception as e:
                    exceptionOrders.append(cancel_size_order)
                    self._logger.warning(f"Failed To Cancel Order,OrderLinkId: {cancel_size_order.order_link_id}"
                                   f",TradeId:{cancel_size_order.tradeId},Symbol:{cancel_size_order.symbol},Error:{e}")

                return exceptionOrders, trade

    def update_trade(self, trade: Trade) -> Trade:
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        try:
            with tradeLock:
                if trade.trade_id in self._open_trades:
                    trade = self._open_trades[trade.trade_id]
                    request: RequestParameters = RequestParameters(broker=trade.relation_id.broker_id,
                                                                   symbol=trade.relation_id.asset, category=trade.category)

                    openAndClosedOrders: list[BrokerOrder] = self.get_open_and_closed_orders(request)

                    for onco in openAndClosedOrders:
                        for order in trade.orders:
                            if order.order_link_id == onco.orderLinkId:
                                self._broker_mapper.map_broker_order_to_order(onco, order)

                    if len(trade.orders) == 0:
                        self._logger.error("Trade has no Orders"
                                     ",TradeId{id}"
                                     ",Symbol:{symbol}".format(id=trade.trade_id, symbol=trade.relation_id.asset), "")

                    remove_error_orders = []

                    for order in trade.orders:
                        request.orderLinkId = order.order_link_id
                        orderHistory: list[BrokerOrder] = self.get_order_history(request)
                        for onco in orderHistory:
                            if order.order_link_id == onco.orderLinkId:
                                self._broker_mapper.map_broker_order_to_order(onco, order)
                        if order.order_result_status is None:
                            remove_error_orders.append(order)

                    for order in remove_error_orders:
                        trade.orders.pop(order)

                    positionInfo: list[BrokerPosition] = self.get_position_info(request)

                    for pi in positionInfo:
                        if pi.symbol == trade.relation_id.asset and pi.category == trade.category:
                            self._broker_mapper.map_broker_position_to_trade(pi, trade)

        except Exception as e:
            self._logger.exception("Something went Wrong with Updating,TradeId: {tradeId}: {e}".format(tradeId=trade.trade_id, e=e))
            return trade