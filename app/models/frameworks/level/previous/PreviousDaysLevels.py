from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level


class PreviousDaysLevels(ILevel):

    def returnLevels(self, candles: list[Candle]) -> list[Level]:
        # Step 1: Extract high and low values from the data points
        allLevel = []
        high = None
        highId = None
        low = None
        lowId = None

        allLevels = []  # Changed to allLevels for C# style

        # Collecting high and low values from each data point
        for candle in candles:
            if high  < candle.high:
                high = candle.high
                highId = candle.id
            if low > candle.low:
                low = candle.low
                lowId = candle.id

        # Step 2: Calculate the overall high and low
        previousDaysHigh = Level(name="PDH", level=high)
        previousDaysHigh.setFibLevel(0.0, "High", [highId])
        previousDaysLow = Level(name="PDL", level=low)
        previousDaysLow.setFibLevel(0.0, "Low", [lowId])

        allLevel.append(previousDaysLow)
        allLevel.append(previousDaysHigh)

        return allLevel
