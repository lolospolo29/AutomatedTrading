import threading

from app.db.DBService import DBService
from app.models.trade import Trade
from app.manager.StrategyManager import StrategyManager
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
            self.openTrades: list[Trade] = []
            self._DBService: DBService = DBService()
            self._StrategyManager: StrategyManager = StrategyManager()
            self._RiskManager: RiskManager = RiskManager()
            self._initialized = True  # Markiere als initialisiert


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
