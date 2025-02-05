from abc import abstractmethod

from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.models.calculators.ProfitStopEntryCalculator import ProfitStopEntryCalculator
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class Strategy:
    def __init__(self,name: str,timeFrames:list[ExpectedTimeFrame],time_windows:list[ITimeWindow]=None):
        self.name: str = name
        self.timeframes: list[ExpectedTimeFrame] = timeFrames
        self.time_windows: list[ITimeWindow] = time_windows

    def return_expected_time_frame(self)->list[ExpectedTimeFrame]:
        return self.timeframes

    def to_dict(self):
        return {
            "Strategy": {
                "name": self.name,
                "timeframes": [timeframe.to_dict() for timeframe in self.timeframes],
                "time_windows": [time_window.to_dict() for time_window in self.time_windows]
            }
        }

    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade:Trade,relation:AssetBrokerStrategyRelation)->StrategyResult:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int,relation:AssetBrokerStrategyRelation,asset_class:str)-> StrategyResult:
        pass
    @abstractmethod
    def is_in_time(self, time)->bool:
        pass
