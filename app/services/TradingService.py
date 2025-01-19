import threading
from typing import Any, Dict

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.strategy.StrategyResult import StrategyResult
from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.monitoring.log_time import log_time
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.services.NewsService import NewsService
from app.monitoring.logging.logging_startup import logger

class TradingService:
    """
    The Trading Service serves as the Interface between the Strategy,Asset and the Trade Manager.
    Manages the Dataflow from Incoming Price Signals and fits it into a Business Logic
    """
    # region Singleton

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradingService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # endregion

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._asset_manager: AssetManager = AssetManager()
            self._trade_manager: TradeManager = TradeManager()
            self._strategy_manager: StrategyManager = StrategyManager()
            self._news_service :NewsService = NewsService()
            #self._news_service.receive_news()
            self._logger = logger
            self._logger.info("TradingService initialized")
            self._initialized = True  # Markiere als initialisiert

    # endregion

    @log_time
    def handle_price_action_signal(self, jsonData: Dict[str, Any]) -> None:
        """
        Handles the Dataflow between Strategy Manager,Asset Manager and Trade Manager.

        :param jsonData: JSON Object from Any Price Signal Services.
        """
        candle: Candle = self._asset_manager.add_candle(jsonData)
        candles : list[Candle] = self._asset_manager.return_candles(candle.asset, candle.broker, candle.timeframe)
        relations: list[AssetBrokerStrategyRelation] = self._asset_manager.return_relations(candle.asset, candle.broker)
        if not self._news_service.is_news_ahead():
            self._analyze_strategy_for_entry(candle.asset, candle.broker, candle.timeframe, candles, relations)

            for relation in relations:
                self._analyze_strategy_for_entry(timeframe=candle.timeframe, candles=candles, relations=relation)

    @log_time
    def _analyze_strategy_for_entry(self, timeframe:int, candles:list[Candle], relation:AssetBrokerStrategyRelation) -> None:
        """
        Analyses Strategy Logic.
        If there is a Signal for a Entry,the Strategy generates a Trade Object.
        That Object is used to Execute Orders in the Trade Manager.

        :param timeframe: Timeframe to analyze.
        :param candles: Candles to analyze.
        :param relation Relation of the Asset,Strategy,Broker
        """

        result: StrategyResult = self._strategy_manager.get_entry(candles, relation, timeframe)

        if result.status == StrategyResultStatusEnum.NEWORDER.value:
            self._logger.info(f"New Entry found: {relation.asset}")

            self._trade_manager.register_trade(result.trade)
            trade = self._trade_manager.return_trades_for_relation(relation)
            # todo order logic and exit logic
