import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel


class STDV(ILevel):
    def __init__(self):
        self.extensionLevels: list[float] = [1.5, 2, 3, 4]
        self.name = "STDV"

    def returnLevels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        # Step 1: Apply lookback to limit the range of candles
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
            if lookback is not None and len(candles) < lookback:
                return []

            allLevel = []
            # Step 2: Calculate Fibonacci levels down to the breaker candle
            high = -1
            highCandle = None
            low = sys.maxsize
            lowCandle = None

            # Collecting high and low values from each data point
            for candle in candles:
                if high < candle.high:
                    high = candle.high
                    highCandle = candle
                if low > candle.low:
                    low = candle.low
                    lowCandle = candle

            candles:list[Candle] = [highCandle, lowCandle]

            fibLevel15Bullish = high - 1.5 * (high - low)
            fibLevel20Bullish = high - 2 * (high - low)
            fibLevel30Bullish = high - 3 * (high - low)
            fibLevel40Bullish = high - 4 * (high - low)

            fibLevel15Bearish = low + 1.5 * (high - low)
            fibLevel20Bearish = low + 2 * (high - low)
            fibLevel30Bearish = low + 3 * (high - low)
            fibLevel40Bearish = low + 4 * (high - low)

            fibLevel15BearishObj = Level(name=self.name, level=fibLevel15Bearish)
            fibLevel15BearishObj.setFibLevel(1.5,"Bearish",candles=candles)
            fibLevel20BearishObj = Level(name=self.name, level=fibLevel20Bearish)
            fibLevel20BearishObj.setFibLevel(2.5,"Bearish",candles=candles)
            fibLevel30BearishObj = Level(name=self.name, level=fibLevel30Bearish)
            fibLevel30BearishObj.setFibLevel(3.0,"Bearish",candles=candles)
            fibLevel40BearishObj = Level(name=self.name, level=fibLevel40Bearish)
            fibLevel40BearishObj.setFibLevel(4.0,"Bearish",candles=candles)

            allLevel.append(fibLevel15BearishObj)
            allLevel.append(fibLevel20BearishObj)
            allLevel.append(fibLevel30BearishObj)
            allLevel.append(fibLevel40BearishObj)

            fibLevel15BullishObj = Level(self.name, level=fibLevel15Bullish)
            fibLevel15BullishObj.setFibLevel(1.5,"Bullish",candles=candles)
            fibLevel20BullishObj = Level(self.name, level=fibLevel20Bullish)
            fibLevel20BullishObj.setFibLevel(2.0,"Bullish",candles=candles)
            fibLevel30BullishObj = Level(self.name, level=fibLevel30Bullish)
            fibLevel30BullishObj.setFibLevel(3.0,"Bullish",candles=candles)
            fibLevel40BullishObj = Level(self.name, level=fibLevel40Bullish)
            fibLevel40BullishObj.setFibLevel(4.0,"Bullish",candles=candles)

            allLevel.append(fibLevel15BullishObj)
            allLevel.append(fibLevel20BullishObj)
            allLevel.append(fibLevel30BullishObj)
            allLevel.append(fibLevel40BullishObj)

            return allLevel