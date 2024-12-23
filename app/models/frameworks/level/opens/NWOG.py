from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level


class NWOG:

    def __init__(self):
        self.name = 'NWOG'

    def returnLevels(self, preCandle: Candle, midNightCandle: Candle) -> list[Level]:
        allLevel = []
        high = None
        highId = None
        low = None
        lowId = None

        if midNightCandle.high > preCandle.high:
            high = midNightCandle.high
            highId = midNightCandle.high

        if preCandle.high > midNightCandle.high:
            high = preCandle.high
            highId = preCandle.high

        if midNightCandle.low < preCandle.low:
            low = midNightCandle.low
            lowId = midNightCandle.low
        if preCandle.low < midNightCandle.low:
            low = preCandle.low
            lowId = preCandle.low

        NWOGHighObj = Level(self.name, level=high)
        NWOGHighObj.setFibLevel(0.0, "High", [highId])
        NWOGLowObj = Level(self.name, level=low)
        NWOGLowObj.setFibLevel(0.0, "Low", [lowId])

        allLevel.append(NWOGHighObj)
        allLevel.append(NWOGLowObj)

        return allLevel
