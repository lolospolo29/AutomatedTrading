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


class TradingService:

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
            self._initialized = True  # Markiere als initialisiert

    # endregion

    @log_time
    def handle_price_action_signal(self, jsonData: Dict[str, Any]) -> None:

        candle: Candle = self._asset_manager.add_candle(jsonData)
        candles : list[Candle] = self._asset_manager.return_candles(candle.asset, candle.broker, candle.timeframe)
        relations: list[AssetBrokerStrategyRelation] = self._asset_manager.return_relations(candle.asset, candle.broker)
        if not self._news_service.is_news_ahead():
            self._analyze_strategy_for_entry(candle.asset, candle.broker, candle.timeframe, candles, relations)

            for relation in relations:
                self._analyze_strategy_for_entry(timeframe=candle.timeframe, candles=candles, relations=relation)


    @log_time
    def _analyze_strategy_for_entry(self, timeframe:int, candles:list[Candle], relation:AssetBrokerStrategyRelation) -> None:

        result: StrategyResult = self._strategy_manager.get_entry(candles, relation, timeframe)

        if result.status == StrategyResultStatusEnum.NEWORDER.value:

            self._trade_manager.register_trade(result.trade)
            trade = self._trade_manager.return_trades_for_relation(relation)
            # todo order logic and exit logic
