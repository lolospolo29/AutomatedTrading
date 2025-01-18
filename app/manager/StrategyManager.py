import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class StrategyManager:

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
            print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")
            return True
        else:
            print(f"Strategy '{strategy.name}' already exists in the Strategy Manager.")
            return False

    def return_expected_time_frame(self, strategy: str) -> list:
        if strategy in self.strategies:
            return self.strategies[strategy].return_expected_time_frame()
        return []

    def get_entry(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                  timeFrame: int) -> StrategyResult:
        if relation.strategy in self.strategies:
            return self.strategies[relation].get_entry(candles, timeFrame)

    def get_exit(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                 timeFrame: int, trade:Trade) -> StrategyResult:
        if relation.strategy in self.strategies:
            return self.strategies[relation].get_exit(candles, timeFrame, trade)
