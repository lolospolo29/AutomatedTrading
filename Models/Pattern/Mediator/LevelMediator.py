from Models.StrategyAnalyse.Levels.CBDR import CBDR
from Models.StrategyAnalyse.Levels.Fibonnaci.OTE import OTE
from Models.StrategyAnalyse.Levels.Fibonnaci.PD import PD
from Models.StrategyAnalyse.Levels.Fibonnaci.STDV import STDV
from Models.StrategyAnalyse.Levels.NDOG import NDOG
from Models.StrategyAnalyse.Levels.NWOG import NWOG
from Models.StrategyAnalyse.Levels.PreviousDaysLevels import PreviousDaysLevels
from Models.StrategyAnalyse.Levels.PreviousSessionLevels import PreviousSessionLevels
from Models.StrategyAnalyse.Levels.PreviousWeekLevels import PreviousWeekLevels
from Models.StrategyAnalyse.Levels.equalHL import equalHL


class LevelMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LevelMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.ote: OTE = OTE()
            self.pd = PD()
            self.stdv = STDV()
            self.cbdr = CBDR()
            self.equal = equalHL()
            self.ndog = NDOG()
            self.nwog = NWOG()
            self.previousDaysLevel = PreviousDaysLevels()
            self.previousSessionLevel = PreviousSessionLevels()
            self.previousWeekLevels = PreviousWeekLevels()

            self.initialized: bool = True  # Mark as initialized

    def calculateLevels(self, levelType: str, candles: list, *args, **kwargs) -> list:
        if levelType == "OTE":
            return self.ote.returnLevels(candles)
        if levelType == "PD":
            self.pd.returnLevels(candles)
        if levelType == "STDV":
            if 'pd' in kwargs:
                addedAttribute = kwargs['pd']
                self.stdv.returnLevels(candles, addedAttribute)
        if levelType == "NWOG":
            self.nwog.returnLevels(candles)
        if levelType == "NDOG":
            self.ndog.returnLevels(candles)
        if levelType == "previousDaysLevels":
            self.previousDaysLevel.returnLevels(candles)
        if levelType == "PreviousSessionLevels":
            self.previousSessionLevel.returnLevels(candles)
        if levelType == "PreviousWeekLevels":
            self.previousWeekLevels.returnLevels(candles)


