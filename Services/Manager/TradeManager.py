from Models.Trade import Trade


class TradeManager:
    def __init__(self, DBService, BrokerManager, StrategyManager, RiskManager):
        self.openTrades: list[Trade] = []
        self._DBService = DBService
        self._BrokerManager = BrokerManager
        self._StrategyManager = StrategyManager
        self._RiskManager = RiskManager

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
