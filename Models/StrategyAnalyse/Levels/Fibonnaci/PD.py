from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class PD(ILevel):
    def __init__(self):
        self.pdLevels: list[float] = [1.0, 0.5, 0]

    def returnLevels(self, candles: list[Candle]) -> list:
        # Step 1: Extract high and low values from the data points
        allHighs = []
        allLows = []
        allLevel = []

        for dataPoint in candles:  # Using camelCase for the variable
            allHighs.extend(dataPoint.high)
            allLows.extend(dataPoint.low)

        # Step 2: Calculate the overall high and low
        high = max(allHighs) if allHighs else 0  # Added a safeguard for empty lists
        low = min(allLows) if allLows else 0

        # Step 3: Calculate the PD levels
        level0 = low  # 0.0 corresponds to the low value
        level1 = high  # 1.0 corresponds to the high value
        level05 = (high + low) / 2  # 0.5 is the midpoint between high and low

        # Step 4: Create Level objects with names "0.0", "0.5", and "1.0"
        level0Obj = Level(name="pd_0.0", level=level0)
        level05Obj = Level(name="pd_0.5", level=level05)
        level1Obj = Level(name="pd_1.0", level=level1)

        allLevel.append(level0Obj)
        allLevel.append(level05Obj)
        allLevel.append(level1Obj)

        # Step 5: Return all three Level objects
        return allLevel
