import threading

from app.api.brokers.BrokerFacade import BrokerFacade
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.RequestParameters import RequestParameters
from app.db.mongodb.mongoDBTrades import mongoDBTrades
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.mappers.ClassMapper import ClassMapper
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from app.monitoring.logging.logging_startup import logger


class TradeManager:

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
            self._open_trades:dict[str,Trade] = {}
            self._mongo_db_trades: mongoDBTrades = mongoDBTrades()
            self._broker_facade = BrokerFacade()
            self._risk_manager = RiskManager()
            self._class_mapper = ClassMapper()
            self._initialized = True  # Markiere als initialisiert
    # endregion

    # region Register Remove Dict
    def register_trade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                self._trade_registry.register_relation(trade.relation)
                self._trade_registry.acquire_trade(trade.relation)
                if trade.id not in self._open_trades:
                    self._open_trades[trade.id] = trade
                    logger.info(f"Trade for '{trade.relation.broker}' "
                          f"with ID: {trade.id} created and added to the Trade Manager.")

    def remove_trade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self._open_trades:
                    self._open_trades.pop(trade.id)
    # endregion

    # region CRUD DB
    def find_trade_or_trades_in_db(self, trade:Trade=None) -> list[Trade]:
        with self._lock:
            if trade is None:
                return self._mongo_db_trades.find_trade_or_trades_by_id()
            else:
                return self._mongo_db_trades.find_trade_or_trades_by_id(trade.id)



    def write_trade_to_db(self, trade: Trade):
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self._open_trades:
                    self._mongo_db_trades.add_trade_to_db(trade)

    def update_trad_in_db(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self._open_trades:
                    self._mongo_db_trades.update_trade(trade)

    def archive_trade_in_db(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self._open_trades:
                    self._mongo_db_trades.archive_trade(trade)

    def find_order_or_orders_in_db(self, order:Order=None) -> list[Order]:
        if order is None:
            return self._mongo_db_trades.find_order_or_orders_by_id()
        else:
            return self._mongo_db_trades.find_order_or_orders_by_id(order.orderLinkId)

    def write_order_to_db(self, order: Order) -> None:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
                self._mongo_db_trades.add_order_to_db(order)

    def update_order_in_db(self, order: Order) -> None:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongo_db_trades.update_order(order)

    def archiveOrderInDB(self, order: Order) -> None:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongo_db_trades.archive_order(order)
    # endregion

    # region API Requests
    def place_trade(self, trade: Trade):
            tradeLock = self._lock_registry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self._open_trades:
                    trade = self._open_trades[trade.id]

                    threads :list[threading.Thread]= []

                    for order in trade.orders:
                        t = threading.Thread(target=self.place_order, args=(trade.relation.broker, order), daemon=True)
                        threads.append(t)

                    for thread in threads:
                        thread.start()

                    while True:
                        done = True
                        for thread in threads:
                            if thread.is_alive():
                                done = False
                        if done:
                            break

    def place_order(self, broker:str, order: Order)->Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder:BrokerOrder = self._broker_facade.place_order(requestParameters)
            order = self._class_mapper.update_class_with_dataclass(newOrder, order)
        return order

    def amend_order(self, broker:str, order:Order)->Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder:BrokerOrder = self._broker_facade.amend_order(requestParameters)
            order = self._class_mapper.update_class_with_dataclass(newOrder, order)
        return order

    def cancel_order(self, broker:str, order:Order)->Order:
        orderLock = self._lock_registry.get_lock(order.orderLinkId)
        with orderLock:
            requestParameters: RequestParameters = (self._class_mapper.map_args_to_dataclass
                                                    (RequestParameters, order, Order, broker=broker))
            newOrder:BrokerOrder = self._broker_facade.amend_order(requestParameters)
            self._class_mapper.update_class_with_dataclass(newOrder, order)
        return order

    def return_open_and_closed_orders(self, requestParameters:RequestParameters) -> list[Order]:
        return self._broker_facade.return_open_and_closed_orders(requestParameters)

    def return_position_info(self, requestParameters:RequestParameters)->Trade:
        return self._broker_facade.return_position_info(requestParameters)

    def return_order_history(self, requestParameters:RequestParameters) -> list[Order]:
        return self._broker_facade.return_order_history(requestParameters)

    # endregion

    # region Functions

    def calculate_qty_for_trade_orders(self, trade:Trade, assetClass:str):
        tradeLock = self._lock_registry.get_lock(trade.id)
        with tradeLock:
            if trade.id in self._open_trades:
                trade = self._open_trades[trade.id]
                for order in trade.orders:
                    if order.orderType == OrderTypeEnum.MARKET.value:
                        order.qty = str(self._risk_manager.calculate_qty_market(assetClass, order))
                    if order.orderType == OrderTypeEnum.LIMIT.value:
                        order.qty = str(self._risk_manager.calculate_qty_limit(assetClass, order))


    def return_all_trades(self)->list[Trade]:
        return [trade for trade in self._open_trades.values()]

    def return_trades_for_relation(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation)->list[Trade]:
        return [x for x in self._open_trades.values() if x.relation.compare(assetBrokerStrategyRelation)]
    # endregion

# todo order builder for every broker
# todo execptions
# tm = TradeManager()
#
# relation = AssetBrokerStrategyRelation("ABC","BYBIT","ABC",2)
# relation2 = AssetBrokerStrategyRelation("ABC","BYBIT","ABC",2)
#
# order = Order()
#
# order.orderType = OrderTypeEnum.MARKET.value
# order.category = "linear"
# order.symbol = "XRPUSDT"
# order.riskPercentage = 0.33
# order.price =str(3.1)
# order.stopLoss = str(2.7)
# order.orderLinkId = "13133"
# order.side = "Buy"
#
# trade = TradeBuilder().add_relation(relation).add_order(order).build()
#
# tm.register_trade(trade)
#
# print(tm.return_trades_for_relation(relation2))
#
# tm.calculate_qty_for_trade_orders(trade,AssetClassEnum.CRYPTO.value)
#
# trades = tm.return_all_trades()
#
# tm.place_trade(trade)
#
# trades = tm.return_all_trades()
#
# print(trades)
