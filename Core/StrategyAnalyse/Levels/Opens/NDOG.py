from Core.Main.Asset import Candle
from Core.StrategyAnalyse.Level import Level
from Interfaces.Strategy.ILevel import ILevel


class NDOG(ILevel):
    def __init__(self):
        self.name = 'NDOG'
    def returnLevels(self, preCandle: Candle, midNighcandle: Candle) -> list:
        allLevel = []
        high = None
        highId = None
        low = None
        lowId = None

        if midNighcandle.high > preCandle.high:
            high = midNighcandle.high
            highId = midNighcandle.high

        if preCandle.high > midNighcandle.High:
            high = preCandle.high
            highId = preCandle.high

        if midNighcandle.low < preCandle.low:
            low = midNighcandle.low
            lowId = midNighcandle.low
        if preCandle.low < midNighcandle.Low:
            low = preCandle.low
            lowId = preCandle.low

        NDOGHighObj = Level(self.name, level=high)
        NDOGHighObj.setFibLevel(0.0,"High",[highId])
        NDOGLowObj = Level(self.name, level=low)
        NDOGLowObj.setFibLevel(0.0,"Low",[lowId])

        allLevel.append(NDOGHighObj)
        allLevel.append(NDOGLowObj)

        return allLevel
