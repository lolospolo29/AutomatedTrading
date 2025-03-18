import threading
from logging import Logger

from files.api.brokers.models.BrokerOrder import BrokerOrder
from files.api.brokers.models.BrokerPosition import BrokerPosition
from files.api.brokers.models.RequestParameters import RequestParameters
from files.db.mongodb.TradeRepository import TradeRepository
from files.db.mongodb.dtos.BrokerDTO import BrokerDTO
from files.db.mongodb.dtos.TradeDTO import TradeDTO
from files.helper.builder.OrderBuilder import OrderBuilder
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.registry.LockRegistry import LockRegistry
from files.helper.registry.SemaphoreRegistry import SemaphoreRegistry
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.RiskManager import RiskManager
from files.mappers.BrokerMapper import BrokerMapper
from files.mappers.ClassMapper import ClassMapper
from files.models.asset.Relation import Relation
from files.models.strategy.OrderResultStatus import OrderResultStatusEnum
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade
from files.models.trade.enums.Side import Side
from files.models.trade.enums.OrderStatus import OrderStatus


class TradeManager:
    """
    Manages trading operations, including initializing necessary components, maintaining
    trade states, and interacting with external systems such as databases and brokers.

    This class is implemented as a thread-safe singleton. It provides interfaces to perform
    trading activities such as registering, removing, updating, and interacting with trades
    and orders in a secure, concurrent environment. Trades and orders are persisted to
    the database and handled with locking mechanisms to ensure consistency and
    prevent race conditions.
    """
    # region Initializing
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(TradeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, trade_repository:TradeRepository, broker_facade:BrokerRegistry, risk_manager:RiskManager
                 , relation_manager:RelationManager,broker_mapper:BrokerMapper,class_mapper:ClassMapper
                 ,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._trade_registry = SemaphoreRegistry()
            self._lock_registry = LockRegistry()
            self._open_trades: dict[str, Trade] = {}
            self._trade_repository: TradeRepository = trade_repository
            self._risk_manager = risk_manager
            self._broker_facade = broker_facade
            self._broker_mapper = broker_mapper
            self._class_mapper = class_mapper
            self._logger = logger
            self._relation_manager = relation_manager
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region In Memory Functions

    def register_trade(self, trade: Trade) -> None:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        with tradeLock:
            try:
                if trade.tradeId not in self._open_trades:
                    self._trade_registry.register_semaphore(trade.relation.__str__())
                    self._trade_registry.acquire_semaphore(trade.relation.__str__())
                    self._open_trades[trade.tradeId] = trade
                    self._logger.info(f"Register Trade,TradeId: {trade.tradeId}")
            except Exception as e:
                self._logger.error(f"Register Trade Error,TradeId: {trade.tradeId}: {e}")

    def __remove_trade(self, trade: Trade) -> None:
        try:
            if trade.tradeId in self._open_trades:
                self._open_trades.pop(trade.tradeId)
                self._trade_registry.release_semaphore(trade.relation)
                self._logger.info(f"Remove Trade,TradeId: {trade.tradeId}")
        except AttributeError as e:
            self._logger.fatal(f"Remove Trade Error,TradeId: {trade.tradeId}: {e}")

    # endregion

    # region CRUD DB

    def get_trades(self)->list[Trade]:
        trade_dtos = self._trade_repository.find_trades()

        trades = []

        for trade_db in trade_dtos:

            trade_db:TradeDTO = trade_db
            orders = []

            orders.extend(self._trade_repository.find_orders_by_trade_id(trade_db.tradeId))

            relation = self._relation_manager.return_relation_for_id(trade_db.relationId)

            trade = Trade(orders=orders, tradeId=trade_db.tradeId, relation=relation, category=trade_db.category
                          , side=trade_db.side, tpslMode=trade_db.tpslMode,
                          unrealisedPnl=trade_db.unrealisedPnl
                          , leverage=trade_db.leverage, size=trade_db.size, tradeMode=trade_db.tradeMode
                          , updatedTime=trade_db.updatedTime, createdTime=trade_db.createdTime)

            trades.append(trade)

        return trades

    def get_brokers(self)->list[BrokerDTO]:
        return self._trade_repository.find_brokers()

    def __write_trade_to_db(self, trade: Trade):
        if trade.tradeId in self._open_trades:
            self._logger.info(f"Write Trade To DB,TradeId: {trade.tradeId}")
            self._trade_repository.add_trade_to_db(trade)

    def __write_order_to_db(self, order: Order) -> None:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            self._logger.info(f"Write Order To DB,OrderLinkId: {order.orderLinkId},TradeId:{order.tradeId},Symbol:{order.symbol}")
            self._trade_repository.add_order_to_db(order)

    def __update_trade_in_db(self, trade: Trade) -> None:
        if trade.tradeId in self._open_trades:
            self._logger.info(f"Update To DB,TradeId: {trade.tradeId}")
            self._trade_repository.update_trade(trade)

    def __update_order_in_db(self, order: Order) -> None:
        self._logger.info(f"Update Order in DB,OrderLinkId: {order.orderLinkId},TradeId:{order.tradeId},Symbol:{order.symbol}")
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            self._trade_repository.update_order(order)

    # endregion

    #region API
    def __place_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.place_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder, order)

    def __amend_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.amend_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder, order)

    def __cancel_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.cancel_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder, order)

    def __set_leverage(self, request_parameters: RequestParameters) -> bool:
        return self._broker_facade.set_leverage(request_parameters)

    def __cancel_all_orders(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_facade.cancel_all_orders(request_parameters)

    def __return_open_and_closed_orders(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_facade.return_open_and_closed_orders(request_parameters)

    def __return_position_info(self, request_parameters: RequestParameters) -> list[BrokerPosition]:
        return self._broker_facade.return_position_info(request_parameters)

    def __return_order_history(self, request_parameters: RequestParameters) -> list[BrokerOrder]:
        return self._broker_facade.return_order_history(request_parameters)

    # endregion

    # region Functions

    def return_trades_for_relation(self, assetBrokerStrategyRelation: Relation) -> list[Trade]:
        trades = []
        for id, trade in self._open_trades.items():
            try:
                if trade.relation == assetBrokerStrategyRelation:
                    trades.append(trade)
            except AttributeError as e:
                self._logger.error("Return Trades Error,Error:{e}".format(e=e))
        return trades

    def return_storage_trades(self) -> list[Trade]:
        trades = []

        for id, trade in self._open_trades.items():
            trades.append(trade)
        return trades

    # endregion

    # region API Requests
    def place_trade(self, trade: Trade) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        with tradeLock:
            if trade.tradeId in self._open_trades:
                trade = self._open_trades[trade.tradeId]

                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        self.__place_order(trade.relation.broker, order)
                    except Exception as e:
                        self._logger.exception(f"Place Order Error,"
                                       f"OrderLinkId: {order.orderLinkId},"
                                       f"TradeId:{order.tradeId},Symbol:{order.symbol},OrderType:{order.orderType},error:{e}")
                        exceptionOrders.append(order)
                        break

                return exceptionOrders, trade

    def amend_trade(self, trade: Trade) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        with tradeLock:
            if trade.tradeId in self._open_trades:
                trade: Trade = self._open_trades[trade.tradeId]

                exception_orders: list[Order] = []

                for order in trade.orders:
                    try:
                        if order.order_result_status == OrderResultStatusEnum.AMEND.value:
                            self.__amend_order(trade.relation.broker, order)
                        if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                            self.__cancel_order(trade.relation.broker, order)
                        if order.order_result_status == OrderResultStatusEnum.NEW.value:
                            self.__place_order(trade.relation.broker, order)
                    except Exception as e:
                        exception_orders.append(order)
                        self._logger.exception("Amending Order Error:{e},OrderLinkId:{id},Order Status:{status},"
                                       "Symbol:{symbol}".format(e=e, id=order.orderLinkI,
                                                                status=order.order_result_status, symbol=order.symbol))
            return exception_orders, trade

    def cancel_trade(self, trade: Trade) -> tuple[list[Order], Trade]:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        with tradeLock:
            if trade.tradeId in self._open_trades:
                trade = self._open_trades[trade.tradeId]
                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        self.__cancel_order(trade.relation.broker, order)
                    except Exception as e:
                        if order.orderStatus == OrderStatus.NEW.value or order.orderStatus == OrderStatus.PARTIALLYFILLED.value or order.orderStatus == OrderStatus.UNTRIGGERED.value:
                            exceptionOrders.append(order)
                            self._logger.error(f"Failed To Cancel Order,Error:{e},OrderLinkId: "
                                         f"{order.orderLinkId},TradeId:{order.tradeId},Symbol:{order.symbol},OrderType:{order.orderType}")

                cancel_size_order = OrderBuilder().create_order(relation=trade.relation, entry_frame_work=None
                                                                , symbol=trade.relation.asset, confirmations=[]
                                                                , category=trade.category, side=trade.side
                                                                , risk_percentage=0, order_number=1
                                                                , tradeId=trade.tradeId).set_defaults(
                                                                  reduce_only=True).build()
                if trade.side == Side.BUY.value:
                    cancel_size_order.side = Side.SELL.value
                if trade.side == Side.SELL.value:
                    cancel_size_order.side = Side.BUY.value
                cancel_size_order.qty = trade.size

                try:
                    if int(cancel_size_order.qty) > 0:
                        trade.orders.append(cancel_size_order)
                        cancel_size_order = self.__place_order(trade.relation.broker, cancel_size_order)
                    else:
                        self._logger.info("Cancel Order Failed due to 0 Qty,OrderLinkId:{id}".format(id=cancel_size_order.tradeId,))
                except Exception as e:
                    exceptionOrders.append(cancel_size_order)
                    self._logger.warning(f"Failed To Cancel Order,OrderLinkId: {cancel_size_order.orderLinkId}"
                                   f",TradeId:{cancel_size_order.tradeId},Symbol:{cancel_size_order.symbol},Error:{e}")

                return exceptionOrders, trade

    def update_trade(self, trade: Trade) -> Trade:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        try:
            with tradeLock:
                if trade.tradeId in self._open_trades:
                    trade = self._open_trades[trade.tradeId]
                    request: RequestParameters = RequestParameters(broker=trade.relation.broker,
                                                                   symbol=trade.relation.asset, category=trade.category)

                    openAndClosedOrders: list[BrokerOrder] = self.__return_open_and_closed_orders(request)

                    for onco in openAndClosedOrders:
                        for order in trade.orders:
                            if order.orderLinkId == onco.orderLinkId:
                                self._broker_mapper.map_broker_order_to_order(onco, order)

                    if len(trade.orders) == 0:
                        self._logger.error("Trade has no Orders"
                                     ",TradeId{id}"
                                     ",Symbol:{symbol}".format(id=trade.tradeId, symbol=trade.relation.asset), "")

                    remove_error_orders = []

                    for order in trade.orders:
                        request.orderLinkId = order.orderLinkId
                        orderHistory: list[BrokerOrder] = self.__return_order_history(request)
                        for onco in orderHistory:
                            if order.orderLinkId == onco.orderLinkId:
                                self._broker_mapper.map_broker_order_to_order(onco, order)
                        if order.order_result_status is None:
                            remove_error_orders.append(order)

                    for order in remove_error_orders:
                        trade.orders.pop(order)

                    positionInfo: list[BrokerPosition] = self.__return_position_info(request)

                    for pi in positionInfo:
                        if pi.symbol == trade.relation.asset and pi.category == trade.category:
                            self._broker_mapper.map_broker_position_to_trade(pi, trade)
                    try:
                        self._trade_repository.update_trade(trade)
                    except Exception:
                        try:
                            self._trade_repository.add_trade_to_db(trade)
                        except Exception as e:
                            self._logger.warning(
                                "Write Trade to DB Error,TradeId: {tradeId}: {e}".format(tradeId=trade.tradeId, e=e))

                    if len(trade.orders) == 0:
                        self._logger.error(
                            "Trade has no Orders,TradeId{id},Symbol:{symbol}".format(id=trade.tradeId,
                                                                                     symbol=trade.relation.asset)
                            , "")
                        raise ValueError("Trade has no Orders")

                    for order in trade.orders:
                        try:
                            self.__update_order_in_db(order)
                        except Exception as e:
                            self._logger.warning("Updating Order In DB Error,OrderLinkId: {orderLinkId}: {e}".format(
                                orderLinkId=order.orderLinkId, e=e))
                            try:
                                self.__write_order_to_db(order)
                                self._trade_repository.add_framework_to_db(order.entry_frame_work)
                                self._trade_repository.add_framework_candles_to_db(framework=order.entry_frame_work)

                            except Exception as e:
                                self._logger.warning("Write Order To DB Error,OrderLinkId: {orderLinkId}: {e}".format(
                                    orderLinkId=order.orderLinkId, e=e))
        except Exception as e:
            self._logger.exception("Something went Wrong with Updating,TradeId: {tradeId}: {e}".format(tradeId=trade.tradeId, e=e))
            self.archive_trade(trade)
            return trade

    def archive_trade(self, trade: Trade) -> None:
        tradeLock = self._lock_registry.get_lock(trade.tradeId)
        with tradeLock:
            if trade.tradeId in self._open_trades:
                trade = self._open_trades[trade.tradeId]
                self.__remove_trade(trade)
                try:
                    self._trade_repository.archive_trade(trade)
                except Exception as e:
                    self._logger.exception(
                        "Something went Wrong with Archiving to DB,TradeId: {tradeId}: {e}".format(tradeId=trade.tradeId, e=e))
                try:
                    for order in trade.orders:
                        try:
                            self._trade_repository.archive_order(order)
                        except Exception as e:
                            self._logger.exception("Archive Order To DB Error,OrderLinkId: {orderLinkId}: {e}".format(
                                orderLinkId=order.orderLinkId, e=e))
                except  Exception as e:
                    self._logger.exception(
                        "Something went Wrong with Archiving Orders,TradeId: {tradeId}: {e}".format(tradeId=trade.tradeId, e=e))
    # endregion