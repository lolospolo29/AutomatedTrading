from Core.Main.Trade import Trade
from Services.DB.DBService import DBService
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.RiskHandler import RiskManager


class TradeManager:
    def __init__(self, dbService: DBService, strategyManager: StrategyManager,
                 riskManager: RiskManager):
        self.openTrades: list[Trade] = []
        self._DBService: DBService = dbService
        self._StrategyManager: StrategyManager = strategyManager
        self._RiskManager: RiskManager = riskManager

    def addTradeToDB(self,trade):
        self._DBService.addTradeToDB(trade)

    def isTradeOpen(self):
        pass

    def handleEntry(self):
        pass

    def handleExit(self):
        pass

    def archiveTrades(self):
        for trade in self.openTrades:
            if trade.status == "closed":
                tradeData = trade.toDict()
                self._DBService.archiveCloseTrade(tradeData)
            if trade.status == "open":
                tradeData = trade.toDict()
                self.addTradeToDB(tradeData)

    def clearOpenTrades(self):
        self.openTrades = []

    def findOpenTrades(self):
        self.openTrades = self._DBService.returnOpenTrades()
