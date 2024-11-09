from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class PD(ILevel):
    def __init__(self):
        self.pdLevels: list[float] = [1.0, 0.5, 0]
        self.name = "PD"

    def returnLevels(self, candles: list[Candle]) -> list:
        # Step 1: Extract high and low values from the data points
        allLevel = []

        # Step 1: Extract high and low values from the data points
        high = None
        highId = None
        low = None
        lowId = None

        for candle in candles:
            if high  < candle.high:
                high = candle.high
                highId = candle.id
            if low > candle.low:
                low = candle.low
                lowId = candle.id

        # Step 3: Calculate the PD levels
        level0 = low  # 0.0 corresponds to the low value
        level1 = high  # 1.0 corresponds to the high value
        level05 = (high + low) / 2  # 0.5 is the midpoint between high and low

        # Step 4: Create Level objects with names "0.0", "0.5", and "1.0"
        level0Obj = Level(name=self.name, level=level0)
        level0Obj.setFibLevel(0.0,"Low",[lowId,highId])
        level05Obj = Level(name=self.name, level=level05)
        level05Obj.setFibLevel(0.5,"Equilibrium",[lowId,highId])
        level1Obj = Level(name=self.name, level=level1)
        level1Obj.setFibLevel(1.0,"High",[lowId,highId])

        allLevel.append(level0Obj)
        allLevel.append(level05Obj)
        allLevel.append(level1Obj)

        # Step 5: Return all three Level objects
        return allLevel
