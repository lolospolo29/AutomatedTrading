import threading

from app.db.DBService import DBService
from app.helper.BrokerFacade import BrokerFacade
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.manager.RiskManager import RiskManager


class TradeManager:

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
            self.openTrades:list[Trade] = []
            self._DBService: DBService = DBService()
            self._BrokerFacade = BrokerFacade()
            self._RiskManager: RiskManager = RiskManager()
            self._initialized = True  # Markiere als initialisiert

    def registerTrade(self, trade: Trade) -> None:
        if len(list(filter(lambda x: x.id == trade.id, self.openTrades))) < 1:
            self.openTrades.append(trade)
            print(f"Trade for '{trade.relation.broker}' with ID: {trade.id} created and added to the Trade Manager.")
            return
        print(f"Trade for '{trade.id}' already exists.")

    def removeTrade(self, trade: Trade) -> None:
        if trade.id in self.openTrades:
            self.openTrades.remove(trade)


    def writeTradeToDB(self, trade: Trade):
        self._DBService.addTradeToDB(trade)

    def updateTradInDB(self, trade: Trade) -> None:
        pass

    def archiveTradeInDB(self, trade: Trade) -> None:
        pass

    def calculateRisk(self,order:Order):
        pass

    def createOrder(self,broker:str,order: Order):
        self._BrokerFacade.sendSingleOrder(broker, order)

    def amendOrder(self,order:Order):
        pass

    def cancelOrder(self, order:Order):
        pass

    def returnCurrentBalance(self):
        pass
    def returnCurrentPnl(self):
        pass

    def isTradeActive(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> bool:
        if len(self.returnTradesForRelation(assetBrokerStrategyRelation)) < 1:
            return False
        return True

    def returnTradesForRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation)->list[Trade]:
        return [x for x in self.openTrades if x.relation.compare(assetBrokerStrategyRelation)]

# t = Trade(AssetBrokerStrategyRelation("BTC","APC","S"),[])
# print(t.id)
# tradeManager = TradeManager()
# tradeManager.registerTrade(t)
# a = tradeManager.returnTrade(AssetBrokerStrategyRelation("BTC","APC","S"))
# for trade in a:
#     print(trade.id)
# tradeManager.registerTrade(t)
