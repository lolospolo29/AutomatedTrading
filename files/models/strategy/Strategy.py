from abc import abstractmethod, ABC
from typing import Optional
from files.models.asset.Relation import Relation
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.models.strategy.StrategyResult import StrategyResult


class Strategy(ABC):
    name:Optional[str]
    timeframes:Optional[list[ExpectedTimeFrame]]

    @abstractmethod
    def is_in_time(self, time) -> bool:
        pass
    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade, relation)->StrategyResult:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int, relation:Relation, asset_class:str)->StrategyResult:
        pass
