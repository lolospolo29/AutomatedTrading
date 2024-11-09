from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class NWOG(ILevel):
    def returnLevels(self, candle: Candle) -> list:
        allLevel = []
        high = candle.high
        low = candle.low

        NWOGHighObj = Level(name="NWOG_high", level=high)
        NWOGLowObj = Level(name="NWOG_low", level=low)

        allLevel.append(NWOGHighObj)
        allLevel.append(NWOGLowObj)

        return allLevel
