from Core.Main.Asset.SubModels import Candle
from Core.Main.Strategy.FrameWorks.Level import Level
from Interfaces.Strategy.ILevel import ILevel


class NWOG(ILevel):
    def __init__(self):
        self.name = 'NWOG'

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

        NWOGHighObj = Level(self.name, level=high)
        NWOGHighObj.setFibLevel(0.0, "High", [highId])
        NWOGLowObj = Level(self.name, level=low)
        NWOGLowObj.setFibLevel(0.0, "Low", [lowId])

        allLevel.append(NWOGHighObj)
        allLevel.append(NWOGLowObj)

        return allLevel
