from abc import abstractmethod
from typing import Optional

from app.helper.calculator.RiskCalculator import RiskCalculator
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.calculators.frameworks.FrameWork import FrameWork
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class Strategy:
    def __init__(self,name: str,timeFrames:list[ExpectedTimeFrame]):
        self.name: str = name
        self.timeFrames: list[ExpectedTimeFrame] = timeFrames
        self.riskCalculator: RiskCalculator = RiskCalculator()

    def return_expected_time_frame(self)->list[ExpectedTimeFrame]:
        return self.timeFrames
    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade:Trade,relation:AssetBrokerStrategyRelation)->StrategyResult:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int,relation:AssetBrokerStrategyRelation,asset_class:str)-> StrategyResult:
        pass
    @abstractmethod
    def is_in_time(self, time)->bool:
        pass
