import threading

from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.strategy.Strategy import Strategy
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger
#from app.services.NewsService import NewsService
from tools.EconomicScrapper.Models.NewsDay import NewsDay


class TradingFacade:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradingFacade, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # endregion

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._asset_manager: AssetManager = AssetManager()
            self._trade_manager: TradeManager = TradeManager()
            self._strategy_manager: StrategyManager = StrategyManager()
            #self._news_service = NewsService()
            self._logger = logger
            self._logger.info("TradingService initialized")
            self._initialized = True  # Markiere als initialisiert

    def get_news_days(self)->list[NewsDay]:
   #     return self._news_service.return_news_days()
         pass
    def get_trades(self)->list[Trade]:
        return self._trade_manager.return_trades()
    def get_assets(self)->list[Asset]:
        return self._asset_manager.return_all_assets()
    def get_strategies(self)->list[Strategy]:
        return self._strategy_manager.return_strategies()



