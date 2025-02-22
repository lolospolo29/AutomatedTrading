from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.models.asset.Relation import Relation
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.StrategyResult import StrategyResult


class Strategy(BaseModel):
    name:Optional[str]=None
    timeframes:Optional[list[ExpectedTimeFrame]]=None
    time_windows:Optional[list[ITimeWindow]]=None

    def is_in_time(self, time) -> bool:
        for time_window in self.time_windows:
            if time_window.is_in_entry_window(time):
                return True

    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade, relation)->StrategyResult:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int, relation:Relation, asset_class:str)->StrategyResult:
        pass
