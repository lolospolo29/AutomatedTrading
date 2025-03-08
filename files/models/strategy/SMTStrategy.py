from abc import abstractmethod

from files.models.asset.Relation import Relation
from files.models.strategy.Strategy import Strategy
from files.models.trade.Trade import Trade
from files.models.strategy.StrategyResult import StrategyResult


class SMTStrategy(Strategy):

    @abstractmethod
    def is_in_time(self, time) -> bool:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int, relation: Relation, asset_class: str) -> StrategyResult:
        pass
    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade: Trade, relation: Relation) -> StrategyResult:
        pass
