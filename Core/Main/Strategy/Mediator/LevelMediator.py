from Core.Main.Asset.SubModels.Candle import Candle
from Core.Main.Strategy.FrameWorks.Levels.CBDR import CBDR
from Core.Main.Strategy.FrameWorks.Levels.Fibonnaci.OTE import OTE
from Core.Main.Strategy.FrameWorks.Levels.Fibonnaci.PD import PD
from Core.Main.Strategy.FrameWorks.Levels.Fibonnaci.STDV import STDV
from Core.Main.Strategy.FrameWorks.Levels.Opens.NDOG import NDOG
from Core.Main.Strategy.FrameWorks.Levels.Opens.NWOG import NWOG
from Core.Main.Strategy.FrameWorks.Levels.Previous.PreviousDaysLevels import PreviousDaysLevels
from Core.Main.Strategy.FrameWorks.Levels.Previous.PreviousSessionLevels import PreviousSessionLevels
from Core.Main.Strategy.FrameWorks.Levels.Previous.PreviousWeekLevels import PreviousWeekLevels
from Core.Main.Strategy.FrameWorks.Levels.equalHL import equalHL


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

    def calculateLevels(self, levelType: str, candles: list[Candle], *args, **kwargs) -> list:
        if levelType == "CBDR":
            return self.cbdr.returnLevels(candles)
        if levelType == "previousDaysLevels":
            return self.previousDaysLevel.returnLevels(candles)
        if levelType == "PreviousSessionLevels":
            return self.previousSessionLevel.returnLevels(candles)
        if levelType == "PreviousWeekLevels":
            return self.previousWeekLevels.returnLevels(candles)

    def calculateEqualLevels(self, candles: list[Candle],direction: str) -> list:
        return self.equal.returnLevels(candles, direction)

    def calculateFibonacci(self,levelType ,candles: list[Candle],lookback) -> list:
        if levelType == "OTE":
            return self.ote.returnLevels(candles,lookback)
        if levelType == "PD":
            return self.pd.returnLevels(candles,lookback)
        if levelType == "STDV":
            return self.stdv.returnLevels(candles,lookback)

    def returnOpeningGap(self,levelType,preCandle,midnightCandle):
        if levelType == "NWOG":
            return self.nwog.returnLevels(preCandle,midnightCandle)
        if levelType == "NDOG":
            return self.ndog.returnLevels(preCandle,midnightCandle)



