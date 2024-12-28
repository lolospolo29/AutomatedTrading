import threading

from app.db.DBService import DBService
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
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
            self.openTrades:dict = {}
            self._DBService: DBService = DBService()
            self._StrategyManager: StrategyManager = StrategyManager()
            self._RiskManager: RiskManager = RiskManager()
            self._initialized = True  # Markiere als initialisiert

    def registerTrade(self, trade: Trade) -> None:
        if trade not in self.openTrades:
            self.openTrades[trade.relation] = trade
            print(f"Trade:'{trade.relation}' created and added to the Trade Manager.")
        else:
            print(f"Trade '{trade.relation}' already exists in the Trade Manager.")

    def isTrade(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> bool:
        if assetBrokerStrategyRelation.strategy not in self.openTrades:
            return False
        return True

    def returnTrade(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> Trade:
        if assetBrokerStrategyRelation.strategy in self.openTrades:
            trade = self.openTrades[assetBrokerStrategyRelation]
            return trade
