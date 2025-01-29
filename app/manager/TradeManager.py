import threading

from app.helper.facade.BrokerFacade import BrokerFacade
from app.api.brokers.BrokerRequestBuilder import BrokerRequestBuilder
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition
from app.api.brokers.models.RequestParameters import RequestParameters
from app.db.mongodb.mongoDBTrades import mongoDBTrades
from app.helper.builder.OrderBuilder import OrderBuilder
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.mappers.BrokerMapper import BrokerMapper
from app.mappers.ClassMapper import ClassMapper
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
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

    :ivar _instance: Singleton instance of the TradeManager.
    :type _instance: TradeManager
    :ivar _lock: Thread lock for concurrent-safe operations.
    :type _lock: threading.Lock
    :ivar _trade_registry: Registry for trade-related semaphore handling.
    :type _trade_registry: TradeSemaphoreRegistry
    :ivar _lock_registry: Registry for lock management associated with trades and orders.
    :type _lock_registry: LockRegistry
    :ivar _open_trades: Dictionary to track active trades by their ID.
    :type _open_trades: dict[str, Trade]
    :ivar _mongo_db_trades: Interface for interacting with the trades collection in MongoDB.
    :type _mongo_db_trades: mongoDBTrades
    :ivar _broker_facade: Facade to abstract broker-specific implementations.
    :type _broker_facade: BrokerFacade
    :ivar _risk_manager: Component to handle risk management logic.
    :type _risk_manager: RiskManager
    :ivar _class_mapper: Mapper utility for reflection-based class identification or matching.
    :type _class_mapper: ClassMapper
    :ivar _broker_mapper: Mapper utility tailored for broker-specific configurations or mappings.
    :type _broker_mapper: BrokerMapper
    :ivar _initialized: Flag to ensure one-time initialization of the instance.
    :type _initialized: bool
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
            self._trade_registry = TradeSemaphoreRegistry()
            self._lock_registry = LockRegistry()
            self._open_trades: dict[str, Trade] = {}
            self._mongo_db_trades: mongoDBTrades = mongoDBTrades()
            self._broker_facade = BrokerFacade()
            self._risk_manager = RiskManager()
            self._class_mapper = ClassMapper()
            self._broker_mapper = BrokerMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Register Remove Dict
    def register_trade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                try:
                    self._trade_registry.register_relation(trade.relation)
                    self._trade_registry.acquire_trade(trade.relation)
                    if trade.id not in self._open_trades:
                        self._open_trades[trade.id] = trade
                        logger.info(f"Register Trade,TradeId: {trade.id}")
                except Exception as e:
                    logger.error(f"Register Trade Error,TradeId: {trade.id}: {e}")

    def __remove_trade(self, trade: Trade) -> None:
        try:
            with self._lock:
                tradeLock = self._lock_registry.get_lock(trade.id)
                with tradeLock:
                    if trade.id in self._open_trades:
                        self._trade_registry.release_trade(trade.relation)
                        self._open_trades.pop(trade.id)
                        logger.info(f"Remove Trade,TradeId: {trade.id}")
        except Exception as e:
            logger.error(f"Remove Trade Error,TradeId: {trade.id}: {e}")

    # endregion

    # region CRUD DB

    def __write_trade_to_db(self, trade: Trade):
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                try:
                    if trade.id in self._open_trades:
                        logger.info(f"Write Trade To DB,TradeId: {trade.id}")
                        self._mongo_db_trades.add_trade_to_db(trade)
                except Exception as e:
                    logger.error(f"Write Trade Error,TradeId: {trade.id}: {e}")
                    raise ValueError(e)

    def __update_trade_in_db(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                try:
                    if trade.id in self._open_trades:
                        logger.info(f"Update To DB,TradeId: {trade.id}")
                        self._mongo_db_trades.update_trade(trade)
                except Exception as e:
                    logger.error(f"Update Trade Error,TradeId: {trade.id}: {e}")
                    raise ValueError(e)

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
                                     f"TradeId:{order.trade_id},Symbol:{order.symbol},OrderType:{order.orderType}")
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
                        logger.warning("Amending Order Error,OrderLinkId:{id},Order Status:{status},"
                                       "Symbol:{symbol}".format(id=order.orderLinkI,
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
                            logger.error(f"Failed To Cancel Order,OrderLinkId: "
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
                    logger.warning(f"Failed To Cancel Order,OrderLinkId: {cancel_size_order.orderLinkId},TradeId:{cancel_size_order.trade_id},Symbol:{cancel_size_order.symbol}")

                return exceptionOrders,trade


    def update_trade(self, trade: Trade) -> Trade:
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                try:
                    trade = self._open_trades[trade.id]
                    request: RequestParameters = BrokerRequestBuilder().set_broker(trade.relation.broker).set_symbol(
                        trade.relation.asset).set_category(trade.category).build()

                    openAndClosedOrders: list[BrokerOrder] = self.__return_open_and_closed_orders(request)

                    for onco in openAndClosedOrders:
                        updatedOrder = False
                        for order in trade.orders:
                            if order.orderLinkId == onco.orderLinkId:
                                updatedOrder = True
                                self._broker_mapper.map_broker_order_to_order(onco, order)
                        #
                        # if not updatedOrder:
                        #     newOrder = Order()
                        #     newOrder = self._broker_mapper.map_broker_order_to_order(onco, newOrder)
                        #     trade.orders.append(newOrder)

                    for order in trade.orders:
                        request.orderLinkId = order.orderLinkId
                        orderHistory:list[BrokerOrder] = self.__return_order_history(request)
                        for onco in orderHistory:
                            if order.orderLinkId == onco.orderLinkId:
                                self._broker_mapper.map_broker_order_to_order(onco, order)


                    positionInfo: list[BrokerPosition] = self.__return_position_info(request)

                    for pi in positionInfo:
                        if pi.symbol == trade.relation.asset and pi.category == trade.category:
                            self._broker_mapper.map_broker_position_to_trade(pi, trade)
                    try:
                        self._mongo_db_trades.update_trade(trade)
                    except Exception as e:
                        try:
                            self._mongo_db_trades.add_trade_to_db(trade)
                        except Exception as e:
                            logger.warning("Write Trade to DB Error,TradeId: {tradeId}: {e}".format(tradeId=trade.id, e=e))
                            raise ValueError("Write Order To DB Error")

                    for order in trade.orders:
                        try:
                            self.__update_order_in_db(order)
                        except Exception as e:
                            try:
                                self.__write_order_to_db(order)
                            except Exception as e:
                                logger.warning("Write Order To DB Error,OrderLinkId: {orderLinkId}: {e}".format(orderLinkId=order.orderLinkId, e=e))
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
                for order in trade.orders:
                    self._mongo_db_trades.archive_order(order)

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

    # region Functions

    def get_current_pnl(self):
        pnl = 0
        for id,trade in self._open_trades:
            pnl += trade.unrealisedPnl()
        self._risk_manager.set_current_pnl(pnl)
        return self._risk_manager.return_current_pnl()

    def return_trades_for_relation(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list[Trade]:
        return [x for x in self._open_trades.values() if x.relation.compare(assetBrokerStrategyRelation)]
    # endregion



# trade_manager = TradeManager()
#
# relation = AssetBrokerStrategyRelation("XRPUSDT", "BYBIT", "ABC", 1)
# relation2 = AssetBrokerStrategyRelation("XRPUSDT", "BYBIT", "ABC", 1)
#
#
# pd = PDArray("A","Buy")
#
# order1 = Order()
# order1.confirmations.append(pd)
#
# order1.orderType = OrderTypeEnum.MARKET.value
# order1.order_result_status = OrderResultStatusEnum.NEW.value
# order1.category = "linear"
# order1.symbol = "XRPUSDT"
# order1.qty = str(3)
# order1.price = str(3.1)
# order1.orderLinkId = uuid.uuid4().__str__()
# order1.side = "Buy"
#
# order2 = Order()
#
# order2.orderType = OrderTypeEnum.LIMIT.value
# order2.category = "linear"
# order2.symbol = "XRPUSDT"
# order2.qty = str(3)
# order2.price = str(3.2)
# order2.triggerPrice = str(3.3)
# order2.triggerDirection = 1
# order2.orderLinkId = uuid.uuid4().__str__()
# order2.side = "Sell"
#
# trade1 = TradeBuilder().add_relation(relation).add_order(order1).add_order(order2).add_category("linear").build()
#
# trade_manager.register_trade(trade1)
#
# print(trade_manager.return_trades_for_relation(relation2))
#
# trades = trade_manager.return_trades_for_relation(relation2)
#
# trade_manager.place_trade(trade1)
#
# trades2 = trade_manager.return_trades_for_relation(relation)
#
# for res1 in trades2:
#     trade_manager.update_trade(res1)
#
# trades3 = trade_manager.return_trades_for_relation(relation)
#
# for res2 in trades3:
#     trade_manager.cancel_trade(res2)
