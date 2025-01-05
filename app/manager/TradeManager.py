import datetime
import threading
from threading import Thread

from app.db.modules.mongoDBTrades import mongoDBTrades
from app.helper.BrokerFacade import BrokerFacade
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.AssetClassEnum import AssetClassEnum
from app.models.trade.Order import Order
from app.models.trade.OrderDirectionEnum import OrderDirection
from app.models.trade.OrderTypeEnum import OrderTypeEnum
from app.models.trade.RequestParameters import RequestParameters
from app.models.trade.Trade import Trade


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
            self._TradeRegistry = TradeSemaphoreRegistry()
            self._LockRegistry = LockRegistry()
            self.openTrades:dict[str,Trade] = {}
            self._mongoDBTrades: mongoDBTrades = mongoDBTrades()
            self._BrokerFacade = BrokerFacade()
            self._RiskManager: RiskManager = RiskManager()
            self._initialized = True  # Markiere als initialisiert
    # endregion

    # region Register Remove Dict
    def registerTrade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                self._TradeRegistry.register_relation(trade.relation)
                self._TradeRegistry.acquire_trade(trade.relation)
                if trade.id not in self.openTrades:
                    self.openTrades[trade.id] = trade
                    print(f"Trade for '{trade.relation.broker}' "
                          f"with ID: {trade.id} created and added to the Trade Manager.")

    def removeTrade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self.openTrades.pop(trade.id)
    # endregion

    # region CRUD DB
    def findTradeOrTradesInDB(self,trade:Trade=None) -> list[Trade]:
        with self._lock:
            if trade is None:
                return self._mongoDBTrades.findTradeOrTradesById()
            else:
                return self._mongoDBTrades.findTradeOrTradesById(trade.id)

    def findOrderOrOrdersInDB(self,order:Order=None) -> list[Order]:
        if order is None:
            return self._mongoDBTrades.findOrderOrOrdersById()
        else:
            return self._mongoDBTrades.findOrderOrOrdersById(order.orderLinkId)

    def writeTradeToDB(self, trade: Trade):
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.addTradeToDB(trade)

    def updateTradInDB(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.updateTrade(trade)

    def archiveTradeInDB(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.archiveTrade(trade)

    def writeOrderToDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
                self._mongoDBTrades.addOrderToDB(order)

    def updateOrderInDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongoDBTrades.updateOrder(order)

    def archiveOrderInDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongoDBTrades.archiveOrder(order)
    # endregion

    # region API Requests
    def placeTrade(self, trade: Trade,assetClass:str) -> None:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    trade = self.openTrades[trade.id]
                    threads = []
                    for order in trade.orders:
                        t:Thread = threading.Thread(target=self.placeOrder, args=(trade.relation.broker,assetClass,order,))
                        threads.append(t)
                    for t in threads:
                        t.start()
                    areThreadsStillActive = False
                    for t in threads:
                        if t.is_alive():
                            areThreadsStillActive = True


    def placeOrder(self,broker:str,assetClass:str,order: Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            if order.orderType == OrderTypeEnum.MARKET.value:
                order.qty = str(self._calculateQtyMarket(assetClass, order))
            if order.orderType == OrderTypeEnum.LIMIT.value:
                order.qty = str(self._calculateQtyLimit(assetClass, order))
            order = self._BrokerFacade.placeOrder(broker, order)

    def amendOrder(self,broker:str,order:Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            order = self._BrokerFacade.amendOrder(broker, order)

    def cancelOrder(self,broker:str,order:Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            order = self._BrokerFacade.amendOrder(broker, order)

    def getPositionInfo(self,broker:str, order:Order,requestParameters:RequestParameters):
        order = self._BrokerFacade.getPositionInfo(broker, order,requestParameters)

    # endregion

    # region Risk Management

    def _calculateQtyMarket(self, assetClass:str, order:Order)->float:
        moneyatrisk = self._RiskManager.calculate_money_at_risk()
        qty = 0.00
        if order.orderType == OrderTypeEnum.MARKET.value:
            if assetClass == AssetClassEnum.CRYPTO.value:
                if order.side == OrderDirection.BUY.value:
                    qty = self._RiskManager.calculate_crypto_trade_size(moneyatrisk,(float(order.price)-float(order.stopLoss)))
                if order.side == OrderDirection.SELL.value:
                    qty = self._RiskManager.calculate_crypto_trade_size(moneyatrisk,(float(order.stopLoss)-float(order.price)))
        return abs(qty)
    def _calculateQtyLimit(self, assetClass:str, order:Order)->float:
        moneyatrisk = self._RiskManager.calculate_money_at_risk()
        qty = 0.00
        if order.orderType == OrderTypeEnum.LIMIT.value:
            if assetClass == AssetClassEnum.CRYPTO:
                if order.side == OrderDirection.BUY.value:
                    qty = (self._RiskManager.calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.price) - float(order.slLimitPrice))))
                if order.side == OrderDirection.SELL.value:
                    qty = (self._RiskManager.calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.slLimitPrice) - float(order.price))))
        return qty

        # todo calculate conditional split orders one tp order one entry one stop loss

    # endregion

    # region Functions
    def returnAllTrades(self)->list[Trade]:
        return [trade for trade in self.openTrades.values()]

    def returnTradesForRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation)->list[Trade]:
        return [x for x in self.openTrades.values() if x.relation.compare(assetBrokerStrategyRelation)]
    # endregion

tm = TradeManager()
order = Order()
order.orderLinkId = "131"
order.category = "linear"
order.symbol = "BTCUSDT"
order.price = str(98000)
order.stopLoss = str(99000)

order.side = OrderDirection.BUY.value
order.orderType = OrderTypeEnum.MARKET.value

relation = AssetBrokerStrategyRelation("ABC","BYBIT","ABC",1)

trade = Trade(relation,[order])
tm.registerTrade(trade)
tm.placeTrade(trade,"Crypto")
