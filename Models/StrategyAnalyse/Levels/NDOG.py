from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class NDOG(ILevel):
    def returnLevels(self, candle: Candle) -> list:
        allLevel = []
        high = candle.high
        low = candle.low

        NDOGHighObj = Level(name="NDOG_high", level=high)
        NDOGLowObj = Level(name="NDOG_low", level=low)

        allLevel.append(NDOGHighObj)
        allLevel.append(NDOGLowObj)

        return allLevel
