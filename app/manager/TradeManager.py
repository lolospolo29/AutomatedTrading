import threading

from app.helper.facade.BrokerFacade import BrokerFacade
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition
from app.api.brokers.models.RequestParameters import RequestParameters
from app.db.mongodb.MongoDBTrades import MongoDBTrades
from app.helper.builder.OrderBuilder import OrderBuilder
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.SemaphoreRegistry import SemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.mappers.BrokerMapper import BrokerMapper
from app.mappers.ClassMapper import ClassMapper
from app.models.asset.Relation import Relation
from app.models.strategy.OrderResultStatusEnum import OrderResultStatusEnum
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.OrderStatusEnum import OrderStatusEnum
from app.monitoring.logging.logging_startup import logger


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
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradeManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._trade_registry = SemaphoreRegistry()
            self._lock_registry = LockRegistry()
            self._open_trades: dict[str, Trade] = {}
            self._mongo_db_trades: MongoDBTrades = MongoDBTrades()
            self._broker_facade = BrokerFacade()
            self._risk_manager = RiskManager()
            self._class_mapper = ClassMapper()
            self._broker_mapper = BrokerMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Register Remove Dict
    def register_trade(self, trade: Trade) -> None:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            try:
                if trade.id not in self._open_trades:
                    self._trade_registry.register_relation(trade.relation.__str__())
                    self._trade_registry.acquire_trade(trade.relation.__str__())
                    self._open_trades[trade.id] = trade
                    logger.info(f"Register Trade,TradeId: {trade.id}")
            except Exception as e:
                logger.error(f"Register Trade Error,TradeId: {trade.id}: {e}")

    def __remove_trade(self, trade: Trade) -> None:
        try:
            if trade.id in self._open_trades:
                self._trade_registry.release_trade(trade.relation)
                self._open_trades.pop(trade.id)
                logger.info(f"Remove Trade,TradeId: {trade.id}")
        except AttributeError as e:
            logger.error(f"Remove Trade Error,TradeId: {trade.id}: {e}")
            self._trade_registry.release_trade(trade.relation)
            self._open_trades.pop(trade)


    # endregion

    # region CRUD DB

    def __write_trade_to_db(self, trade: Trade):
        if trade.id in self._open_trades:
            logger.info(f"Write Trade To DB,TradeId: {trade.id}")
            self._mongo_db_trades.add_trade_to_db(trade)

    def __update_trade_in_db(self, trade: Trade) -> None:
        if trade.id in self._open_trades:
            logger.info(f"Update To DB,TradeId: {trade.id}")
            self._mongo_db_trades.update_trade(trade)

    def __write_order_to_db(self, order: Order) -> None:
        logger.info(f"Write Order To DB,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol}")
        try:
            orderLock = self._lock_registry.get_lock(order.orderLinkId)
            with orderLock:
                self._mongo_db_trades.add_order_to_db(order)
        except Exception as e:
            logger.error(f"Write Order To DB Error,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol}")
            raise ValueError(e)

    def __update_order_in_db(self, order: Order) -> None:
        logger.info(f"Update Order in DB,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol}")
        try:
            orderLock = self._lock_registry.get_lock(order.orderLinkId)
            with orderLock:
                self._mongo_db_trades.update_order(order)
        except Exception as e:
            logger.error(f"Update Order DB Error,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol}")
            raise ValueError(e)

    # endregion

    # region API Requests
    def place_trade(self, trade: Trade) -> tuple[list[Order],Trade]:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                trade = self._open_trades[trade.id]

                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        self.__place_order(trade.relation.broker, order)
                    except Exception as e:
                        logger.warning(f"Place Order Error,"
                                     f"OrderLinkId: {order.orderLinkId},"
                                     f"TradeId:{order.trade_id},Symbol:{order.symbol},OrderType:{order.orderType},error:{e}")
                        exceptionOrders.append(order)
                        break

                return exceptionOrders,trade
    def amend_trade(self, trade: Trade) -> tuple[list[Order],Trade]:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                trade:Trade = self._open_trades[trade.id]

                exception_orders: list[Order] = []

                for order in trade.orders:
                    try:
                        if order.order_result_status == OrderResultStatusEnum.AMEND.value:
                            self.__amend_order(trade.relation.broker,order)
                        if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                            self.__cancel_order(trade.relation.broker,order)
                        if order.order_result_status == OrderResultStatusEnum.NEW.value:
                           self.__place_order(trade.relation.broker,order)
                    except Exception as e:
                        exception_orders.append(order)
                        logger.warning("Amending Order Error:{e},OrderLinkId:{id},Order Status:{status},"
                                       "Symbol:{symbol}".format(e=e,id=order.orderLinkI,
                                                                status=order.order_result_status,symbol=order.symbol))
            return exception_orders,trade

    def cancel_trade(self, trade: Trade) -> tuple[list[Order],Trade]:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                trade = self._open_trades[trade.id]
                exceptionOrders: list[Order] = []

                for order in trade.orders:
                    try:
                        self.__cancel_order(trade.relation.broker, order)
                    except Exception as e:
                        if order.orderStatus == OrderStatusEnum.NEW.value or order.orderStatus == OrderStatusEnum.PARTIALLYFILLED.value or order.orderStatus == OrderStatusEnum.UNTRIGGERED.value:
                            exceptionOrders.append(order)
                            logger.error(f"Failed To Cancel Order,Error:{e},OrderLinkId: "
                                         f"{order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol},OrderType:{order.orderType}")

                # close position order

                cancel_size_order = OrderBuilder().create_order(relation=trade.relation,entry_frame_work=None
                                                                ,symbol=trade.relation.asset,confirmations=[]
                                                                ,category=trade.category,side=trade.side
                                                                ,risk_percentage=0,order_number=1
                                                                ,trade_id=trade.id).set_defaults(reduce_only=True).build()
                if trade.side == OrderDirectionEnum.BUY.value:
                    cancel_size_order.side = OrderDirectionEnum.SELL.value
                if trade.side == OrderDirectionEnum.SELL.value:
                    cancel_size_order.side = OrderDirectionEnum.BUY.value
                cancel_size_order.qty = trade.size

                try:
                    trade.orders.append(cancel_size_order)
                    cancel_size_order = self.__place_order(trade.relation.broker,cancel_size_order)
                except Exception as e:
                    exceptionOrders.append(cancel_size_order)
                    logger.warning(f"Failed To Cancel Order,OrderLinkId: {cancel_size_order.orderLinkId}"
                                   f",TradeId:{cancel_size_order.trade_id},Symbol:{cancel_size_order.symbol},Error:{e}")

                return exceptionOrders,trade


    def update_trade(self, trade: Trade) -> Trade:
        tradeLock = self._lock_registry.get_lock(trade.id)
        try:
            with tradeLock:
                if trade.id in self._open_trades:
                        trade = self._open_trades[trade.id]
                        request:RequestParameters = RequestParameters(broker=trade.relation.broker,symbol=trade.relation.asset,category=trade.category)

                        openAndClosedOrders: list[BrokerOrder] = self.__return_open_and_closed_orders(request)

                        for onco in openAndClosedOrders:
                            for order in trade.orders:
                                if order.orderLinkId == onco.orderLinkId:
                                    self._broker_mapper.map_broker_order_to_order(onco, order)

                        if len(trade.orders) == 0:
                            logger.error("Trade has no Orders"
                                         ",TradeId{id}"
                                         ",Symbol:{symbol}".format(id=trade.id,symbol=trade.relation.asset),"")

                            raise ValueError("Trade has no Orders")

                        remove_error_orders = []

                        for order in trade.orders:
                            request.orderLinkId = order.orderLinkId
                            orderHistory:list[BrokerOrder] = self.__return_order_history(request)
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
                            self._mongo_db_trades.update_trade(trade)
                        except Exception:
                            try:
                                self._mongo_db_trades.add_trade_to_db(trade)
                            except Exception as e:
                                logger.warning("Write Trade to DB Error,TradeId: {tradeId}: {e}".format(tradeId=trade.id, e=e))

                        if len(trade.orders) == 0:
                            logger.error(
                                "Trade has no Orders,TradeId{id},Symbol:{symbol}".format(id=trade.id,
                                                                                         symbol=trade.relation.asset)
                                , "")
                            raise ValueError("Trade has no Orders")

                        for order in trade.orders:
                            try:
                                self.__update_order_in_db(order)
                            except Exception:
                                try:
                                    self.__write_order_to_db(order)
                                except Exception as e:
                                    logger.warning("Write Order To DB Error,OrderLinkId: {orderLinkId}: {e}".format(orderLinkId=order.orderLinkId, e=e))
        except ValueError as e:
            logger.warning("Something went Wrong with Updating,TradeId: {tradeId}: {e}".format(tradeId=trade.id, e=e))
            self.archive_trade(trade)
            return trade
        except Exception as e:
                logger.warning("Something went Wrong with Updating,TradeId: {tradeId}: {e}".format(tradeId=trade.id, e=e))
                return trade

    def archive_trade(self, trade: Trade) -> None:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                trade = self._open_trades[trade.id]
                self._mongo_db_trades.archive_trade(trade)
                self.__remove_trade(trade)
                try:
                    for order in trade.orders:
                        try:
                            self._mongo_db_trades.archive_order(order)
                        except Exception as e:
                            logger.warning("Archive Order To DB Error,OrderLinkId: {orderLinkId}: {e}".format(orderLinkId=order.orderLinkId, e=e))
                except  Exception as e:
                    logger.warning("Something went Wrong with Archiving,TradeId: {tradeId}: {e}".format(tradeId=trade.id, e=e))
    #region API
    def __place_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.place_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder,order)

    def __amend_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.amend_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder,order)

    def __cancel_order(self, broker: str, order: Order) -> Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder: BrokerOrder = self._broker_facade.cancel_order(requestParameters)
            return self._broker_mapper.map_broker_order_to_order(newOrder,order)

    def __set_leverage(self, request_parameters:RequestParameters) -> bool:
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
    # endregion

    # region Functions

    def get_current_pnl(self):
        pnl = 0
        for id,trade in self._open_trades:
            pnl += trade.unrealisedPnl()
        self._risk_manager.set_current_pnl(pnl)
        return self._risk_manager.return_current_pnl()

    def return_trades_for_relation(self, assetBrokerStrategyRelation: Relation) -> list[Trade]:
        trades = []
        for id,trade in self._open_trades:
            try:
                if trade.relation == assetBrokerStrategyRelation:
                    trades.append(trade)
            except AttributeError as e:
                logger.error("Return Trades Error,Error:{e}".format(e=e))
                self.archive_trade(trade)
        return trades



    def return_trades(self) -> list[Trade]:
        t1 = Trade(relation=Relation(asset="a",broker="a",strategy="a",max_trades=1,id=1))
        self.register_trade(t1)
        # todo remove after testing
        return [x for x in self._open_trades.values()]
    # endregion

    # todo test pydantic
