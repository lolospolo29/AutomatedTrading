import threading

from app.db.modules.mongoDBTrades import mongoDBTrades
from app.helper.BrokerFacade import BrokerFacade
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade.Order import Order
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

    def createOrder(self,broker:str,order: Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            self._BrokerFacade.sendSingleOrder(broker, order)

    def amendOrder(self,order:Order):
        pass

    def cancelOrder(self, order:Order):
        pass

    def calculateRisk(self,order:Order):
        pass

    def getPositionInfo(self, order:Order):
        pass

    def returnTradePnl(self, trade:Trade):
        pass

    def returnOrdersStatus(self,trade:Trade):
        pass

    def returnOrdersPnl(self, trade:Trade):
        pass

    def returnAllTrades(self):
        pass

    def returnTradesForRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation)->list[Trade]:
        return [x for x in self.openTrades if x.relation.compare(assetBrokerStrategyRelation)]

    def isTradeActive(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> bool:
        if len(self.returnTradesForRelation(assetBrokerStrategyRelation)) < 1:
            return False
        return True
