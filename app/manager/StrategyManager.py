import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class StrategyManager:
    """Serves as Accessor for Strategy and Storage Access"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(StrategyManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.strategies: dict[AssetBrokerStrategyRelation,Strategy] = {}
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def register_strategy(self, relation:AssetBrokerStrategyRelation, strategy:Strategy) -> bool:
        if relation not in self.strategies:
            self.strategies[relation] = strategy
            logger.info(f"Strategy {strategy.name} registered for relation {relation}")
            return True
        else:
            logger.info(f"Strategy {strategy.name} already registered")
            return False

    def return_expected_time_frame(self, strategy: str) -> list:
        try:
            if strategy in self.strategies:
                logger.info(f"Strategy {strategy} get Expected TimeFrame")
                return self.strategies[strategy].return_expected_time_frame()
            return []
        except Exception as e:
            logger.exception(f"Return Timeframe for {strategy} failed: {e}")

    def get_entry(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                  timeFrame: int) -> StrategyResult:
        try:
            if relation.strategy in self.strategies:
                logger.info(f"Strategy {relation.asset} get Exit TimeFrame")
                return self.strategies[relation].get_entry(candles, timeFrame)
        except Exception as e:
            logger.exception(f"Get Entry Failed for {relation.strategy}/{relation.asset}: {e}")

    def get_exit(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                 timeFrame: int, trade:Trade) -> StrategyResult:
        try:
            if relation.strategy in self.strategies:
                logger.info(f"Strategy {relation.asset} get Exit TimeFrame,TradeId: {trade.id}")
                return self.strategies[relation].get_exit(candles, timeFrame, trade)
        except Exception as e:
            logger.exception(f"Get Exit Failed for {relation.strategy}/{relation}: {e}")
