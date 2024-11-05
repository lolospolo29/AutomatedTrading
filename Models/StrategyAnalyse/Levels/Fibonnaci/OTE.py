from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class OTE(ILevel):
    def __init__(self):
        # Fibonacci retracement levels to calculate
        self.retracementLevels: list[float] = [0.75, 0.62]

    def getLevels(self, candles: list[Candle]) -> list[Level]:
        # Step 1: Extract high and low values from the data points
        allHighs = []
        allLows = []

        allLevels = []  # Changed to allLevels for C# style

        # Collecting high and low values from each data point
        for data_point in candles:
            allHighs.extend(data_point.high)
            allLows.extend(data_point.low)

        # Step 2: Calculate the overall high and low
        high = max(allHighs) if allHighs else 0
        low = min(allLows) if allLows else 0

        # Step 3: Calculate Bearish Fibonacci retracement levels (from high to low)
        level075Bearish = high - 0.75 * (high - low)
        level062Bearish = high - 0.62 * (high - low)

        # Step 4: Calculate Bullish Fibonacci retracement levels (from low to high)
        level075Bullish = low + 0.75 * (high - low)
        level062Bullish = low + 0.62 * (high - low)

        # Step 5: Create Level objects for each Fibonacci level with bullish/bearish names
        level075BearishObj = Level(name="0.75_bearish", level=level075Bearish)
        level062BearishObj = Level(name="0.62_bearish", level=level062Bearish)
        level075BullishObj = Level(name="0.75_bullish", level=level075Bullish)
        level062BullishObj = Level(name="0.62_bullish", level=level062Bullish)

        allLevels.append(level075BearishObj)
        allLevels.append(level062BearishObj)
        allLevels.append(level075BullishObj)
        allLevels.append(level062BullishObj)

        # Step 6: Return all four Level objects
        return allLevels
