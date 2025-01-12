from abc import abstractmethod

from app.helper.calculator.RiskCalculator import RiskCalculator
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class Strategy:
    def __init__(self,name: str,timeFrames:list[ExpectedTimeFrame]):
        self.name: str = name
        self.timeFrames: list[ExpectedTimeFrame] = timeFrames
        self.riskCalculator: RiskCalculator = RiskCalculator()

    def returnExpectedTimeFrame(self)->list[ExpectedTimeFrame]:
        return self.timeFrames
    @abstractmethod
    def getExit(self, candles: list, timeFrame: int,trade:Trade)->StrategyResult:
        pass
    @abstractmethod
    def getEntry(self, candles: list, timeFrame: int)-> StrategyResult:
        pass
    @abstractmethod
    def isInTime(self,time)->bool:
        pass
