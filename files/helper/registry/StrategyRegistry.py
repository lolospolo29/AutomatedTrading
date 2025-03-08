import threading

from files.models.asset.Relation import Relation
from files.models.asset.Candle import Candle
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.models.strategy.Strategy import Strategy
from files.models.strategy.StrategyResult import StrategyResult
from files.models.trade.Trade import Trade
from files.monitoring.logging.logging_startup import logger


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
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(StrategyManager, cls).__new__(cls)
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

    def register_strategy(self, relation:Relation, strategy:Strategy) -> bool:
        if relation not in self.strategies:
            self.strategies[relation] = strategy
            logger.info(f"Strategy {strategy.name} registered for relation {relation}")
            return True
        else:
            logger.info(f"Strategy {strategy.name} already registered")
            return False

    def update_relation(self,relation:Relation):
            for relation_, strategy in self.strategies.items():
                if relation_.id == relation.id:
                    self.delete_strategy(relation_)
                    self.register_strategy(relation,strategy)
                    logger.info(f"Strategy {relation_.asset} updated")
                    return
                    # update the relation not strategy with the input relation

    def delete_strategy(self,relation:Relation):
        try:
            if relation in self.strategies:
                del self.strategies[relation]
                logger.info(f"Strategy {relation.asset} deleted")
        except Exception as e:
            logger.exception("Failed to delete strategy {strategy},Error:{e}".format(strategy=relation, e=e))

    def return_strategies(self)->list[str]:
        return [x.name for x in self.strategies.values()]

    def return_expected_time_frame(self, relation: Relation) -> list[ExpectedTimeFrame]:
        try:
            if relation in self.strategies:
                return self.strategies[relation].timeframes
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
