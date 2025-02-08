from abc import abstractmethod, ABC

from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.models.asset.Relation import Relation
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame


class Strategy(ABC):
    name:str
    timeframes:list[ExpectedTimeFrame]
    time_windows:list[ITimeWindow]

    def is_in_time(self, time) -> bool:
        for time_window in self.time_windows:
            if time_window.is_in_entry_window(time):
                return True

    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade, relation):
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int, relation:Relation, asset_class:str):
        pass
