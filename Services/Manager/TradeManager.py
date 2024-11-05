from Models.Main.Trade import Trade
from Services.DBService import DBService
from Services.Manager.BrokerManager import BrokerManager
from Services.Manager.RiskManager import RiskManager
from Services.Manager.StrategyManager import StrategyManager


class TradeManager:
    def __init__(self, dbService: DBService, brokerManager: BrokerManager, strategyManager: StrategyManager,
                 riskManager: RiskManager):
        self.openTrades: list[Trade] = []
        self._DBService: DBService = dbService
        self._BrokerManager: BrokerManager = brokerManager
        self._StrategyManager: StrategyManager = strategyManager
        self._RiskManager: RiskManager = riskManager

    def addTradeToDB(self, status, trade):
        pass

    def isTradeOpen(self):
        pass

    def handleEntry(self):
        pass

    def handleExit(self):
        pass

    def archiveClosedTrades(self):
        for trade in self.openTrades:
            if trade.status == "closed":
                tradeData = trade.toDict()
                self._DBService.archiveCloseTrade(tradeData)

    def clearOpenTrades(self):
        self.openTrades = []

    def findOpenTrades(self):
        self.openTrades = self._DBService.returnOpenTrades()
