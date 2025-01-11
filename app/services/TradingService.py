import threading
from typing import Any, Dict

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.monitoring.TimeWrapper import logTime
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager


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
            self._AssetManager: AssetManager = AssetManager()
            self._TradeManager: TradeManager = TradeManager()
            self._StrategyManager: StrategyManager = StrategyManager()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    @logTime
    def handlePriceActionSignal(self, jsonData: Dict[str, Any]) -> None:

        candle: Candle = self._AssetManager.addCandle(jsonData)
        candles : list[Candle] = self._AssetManager.returnCandles(candle.asset,candle.broker,candle.timeFrame)
        relations: list[AssetBrokerStrategyRelation] = self._AssetManager.returnRelations(candle.asset, candle.broker)
        self.analyzeStrategy(candle.asset,candle.broker,candle.timeFrame, candles,relations)


    @logTime
    def analyzeStrategy(self, timeFrame:int,candles:list[Candle],
                        relations:list[AssetBrokerStrategyRelation]) -> None:

        # Analyze Foreach strategy that correlates with Broker

        for relation in relations:
            self._StrategyManager.getEntry(candles, relation, timeFrame)

            # todo order logic and exit logic
