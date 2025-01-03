import sys

from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel


class OTE(ILevel):
    def __init__(self):
        # Fibonacci retracement levels to calculate
        self.retracementLevels: list[float] = [0.75, 0.62]
        self.name = "OTE"

    def returnLevels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
        if lookback is not None and len(candles) < lookback:
            return []
        # Step 1: Extract high and low values from the data points
        high = -1
        highId = -1
        low = sys.maxsize
        lowId = -1

        allLevels = []  # Changed to allLevels for C# style

        # Collecting high and low values from each data point
        for candle in candles:
            if high  < candle.high:
                high = candle.high
                highId = candle.id
            if low > candle.low:
                low = candle.low
                lowId = candle.id

        # Step 3: Calculate Bearish Fibonacci retracement levels (from high to low)
        level075Bullish = high - 0.75 * (high - low)
        level062Bullish = high - 0.62 * (high - low)

        # Step 4: Calculate Bullish Fibonacci retracement levels (from low to high)
        level075Bearish = low + 0.75 * (high - low)
        level062Bearish = low + 0.62 * (high - low)

        # Step 5: Create Level objects for each Fibonacci level with bullish/bearish names
        level075BearishObj = Level(name=self.name, level=level075Bearish)
        level075BearishObj.setFibLevel(0.75,"Bearish", [lowId,highId])
        level062BearishObj = Level(name=self.name, level=level062Bearish)
        level062BearishObj.setFibLevel(0.62,"Bearish", [lowId,highId])
        level075BullishObj = Level(name=self.name, level=level075Bullish)
        level075BullishObj.setFibLevel(0.75,"Bullish", [lowId,highId])
        level062BullishObj = Level(name=self.name, level=level062Bullish)
        level062BullishObj.setFibLevel(0.62,"Bullish", [lowId,highId])

        allLevels.append(level075BearishObj)
        allLevels.append(level062BearishObj)
        allLevels.append(level075BullishObj)
        allLevels.append(level062BullishObj)

        # Step 6: Return all four Level objects
        return allLevels
