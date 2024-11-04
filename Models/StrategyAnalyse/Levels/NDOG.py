from Interfaces.Strategy.ILevel import ILevel
from Models.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class NDOG(ILevel):
    def getLevels(self, candle: Candle) -> list[Level]:
        allLevel = []
        high = candle.high
        low = candle.low

        NDOGHighObj = Level(name="NDOG_high", level=high)
        NDOGLowObj = Level(name="NDOG_low", level=low)

        allLevel.append(NDOGHighObj)
        allLevel.append(NDOGLowObj)

        return allLevel
