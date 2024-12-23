from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level


class CBDR(ILevel):
    def __init__(self):
        self.name = 'CBDR'

    def returnLevels(self, candles: list[Candle]) -> list:
        allLevel = []

        high = None
        highId = None
        low = None
        lowId = None

        # Collecting high and low values from each data point
        for candle in candles:
            if high < candle.high:
                high = candle.high
                highId = candle.id
            if low > candle.low:
                low = candle.low
                lowId = candle.id

        cbdrRange = high - low

        cbdRange1BullishObj = Level(name=self.name, level=low - cbdrRange)
        cbdRange1BullishObj.setFibLevel(1,"Bullish",[highId,lowId])
        cbdRange2BullishObj = Level(name=self.name, level=low - cbdrRange - cbdrRange)
        cbdRange2BullishObj.setFibLevel(2,"Bullish",[highId,lowId])
        cbdRange3BullishObj = Level(name=self.name, level=low - cbdrRange - cbdrRange - cbdrRange)
        cbdRange3BullishObj.setFibLevel(3,"Bullish",[highId,lowId])

        cbdRange1BearishObj = Level(self.name, level=low - cbdrRange)
        cbdRange1BearishObj.setFibLevel(1,"Bearish",[highId,lowId])
        cbdRange2BearishObj = Level(self.name, level=low - cbdrRange - cbdrRange)
        cbdRange2BearishObj.setFibLevel(2,"Bearish",[highId,lowId])
        cbdRange3BearishObj = Level(self.name, level=low - cbdrRange - cbdrRange - cbdrRange)
        cbdRange3BearishObj.setFibLevel(3,"Bearish",[highId,lowId])

        allLevel.append(cbdRange1BullishObj)
        allLevel.append(cbdRange2BullishObj)
        allLevel.append(cbdRange3BullishObj)

        allLevel.append(cbdRange1BearishObj)
        allLevel.append(cbdRange2BearishObj)
        allLevel.append(cbdRange3BearishObj)

        return allLevel
