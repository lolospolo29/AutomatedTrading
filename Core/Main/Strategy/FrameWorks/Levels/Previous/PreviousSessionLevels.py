from Core.Main.Asset.SubModels import Candle
from Core.Main.Strategy.FrameWorks.Level import Level
from Interfaces.Strategy.ILevel import ILevel


class PreviousSessionLevels(ILevel):
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

        previousSessionHigh = Level(name="PSH", level=high)
        previousSessionHigh.setFibLevel(0.0, "High", [highId])
        previousSessionLow = Level(name="PSL", level=low)
        previousSessionLow.setFibLevel(0.0, "Low", [lowId])

        allLevel.append(previousSessionHigh)
        allLevel.append(previousSessionLow)

        return allLevel
