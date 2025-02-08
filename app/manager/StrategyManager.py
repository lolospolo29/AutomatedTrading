import threading

from app.models.asset.Relation import Relation
from app.models.asset.Candle import Candle
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class StrategyManager:
    """
    Manages strategy instances for asset-broker relations.

    StrategyManager provides a singleton implementation to manage and interact
    with trading strategies associated with specific asset-broker relations.
    It offers methods to register new strategies and retrieve expected insights
    or actions (e.g., entry or exit strategies) based on provided data.

    :ivar strategies: Dictionary mapping AssetBrokerStrategyRelation instances
                      to their associated Strategy instances.
    :type strategies: dict[Relation, Strategy]
    """

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
            self.strategies: dict[Relation,Strategy] = {}
            self._initialized = True  # Markiere als initialisiert

    # endregion
    def register_smt_strategy(self, relation_smt:Relation, strategy_smt:Strategy, asset2:str) -> bool:
        if relation_smt not in self.strategies:
            for relation, strategy in self.strategies.items():  # Iteriere durch Relation-Struktur und Strategien
                if relation.asset == asset2:  # Prüfe, ob die Relation das gewünschte Asset enthält
                    self.strategies[relation_smt] = strategy
                    return True
            self.strategies[relation_smt] = strategy_smt
            logger.info(f"Strategy {strategy_smt.name} registered for relation {relation_smt}")
            return True
        else:
            logger.info(f"Strategy {strategy_smt.name} already registered")
            return False

    def return_strategies(self)->list[Strategy]:
        return [x for x in self.strategies.values()]

    def register_strategy(self, relation:Relation, strategy:Strategy) -> bool:
        if relation not in self.strategies:
            self.strategies[relation] = strategy
            logger.info(f"Strategy {strategy.name} registered for relation {relation}")
            return True
        else:
            logger.info(f"Strategy {strategy.name} already registered")
            return False

    def return_expected_time_frame(self, relation: Relation) -> list:
        try:
            if relation in self.strategies:
                return self.strategies[relation].time_windows
            return []
        except Exception as e:
            logger.exception(f"Return Timeframe for {relation} failed: {e}")

    def get_entry(self, candles: list[Candle], relation: Relation,
                  timeFrame: int, asset_class:str) -> StrategyResult:
        try:
            if relation in self.strategies:
                logger.info(f"Strategy {relation.asset} get Entry")
                return self.strategies[relation].get_entry(candles, timeFrame,relation,asset_class)
        except Exception as e:
            logger.exception(f"Get Entry Failed for {relation.strategy}/{relation.asset}: {e}")

    def get_exit(self, candles: list[Candle], relation: Relation,
                 timeFrame: int, trade:Trade) -> StrategyResult:
        try:
            if relation in self.strategies:
                logger.info(f"Strategy {relation.asset} get Exit TimeFrame,TradeId: {trade.id}")
                return self.strategies[relation].get_exit(candles, timeFrame, trade,relation)
        except Exception as e:
            logger.exception(f"Get Exit Failed for {relation.strategy}/{relation}: {e}")
