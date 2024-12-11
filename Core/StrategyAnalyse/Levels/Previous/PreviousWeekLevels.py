from Core.Main.Asset import Candle
from Core.StrategyAnalyse.Level import Level
from Interfaces.Strategy.ILevel import ILevel


class PreviousWeekLevels(ILevel):
    def returnLevels(self, candles: list[Candle]) -> list:
        allLevel = []

        high = None
        highId = None
        low = None
        lowId = None

        allLevels = []  # Changed to allLevels for C# style

        # Collecting high and low values from each data point
        for candle in candles:
            if high < candle.high:
                high = candle.high
                highId = candle.id
            if low > candle.low:
                low = candle.low
                lowId = candle.id

        # Step 2: Calculate the overall high and low

        previousWeekHigh = Level(name="PWH", level=high)
        previousWeekHigh.setFibLevel(0.0, "High", [highId])
        previousWeekLow = Level(name="PWL", level=low)
        previousWeekLow.setFibLevel(0.0, "Low", [lowId])

        allLevel.append(previousWeekHigh)
        allLevel.append(previousWeekLow)

        return allLevel
