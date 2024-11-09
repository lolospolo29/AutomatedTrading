from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class PreviousDaysLevels(ILevel):
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

        PDHObj = Level(name="PDH", level=high)
        PDLObj = Level(name="PDL", level=low)

        allLevel.append(PDHObj)
        allLevel.append(PDLObj)

        return allLevel
