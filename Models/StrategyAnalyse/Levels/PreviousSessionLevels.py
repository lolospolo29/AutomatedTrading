from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class PreviousSessionLevels(ILevel):
    def returnLevels(self, candles: list[Candle]) -> list:
        allHighs = []
        allLows = []
        allLevel = []

        for dataPoint in candles:  # Using camelCase for the variable
            allHighs.extend(dataPoint.high)
            allLows.extend(dataPoint.low)

        # Step 2: Calculate the overall high and low
        high = max(allHighs) if allHighs else 0  # Added a safeguard for empty lists
        low = min(allLows) if allLows else 0

        PSHObj = Level(name="PSH", level=high)
        PSLObj = Level(name="PSL", level=low)

        allLevel.append(PSHObj)
        allLevel.append(PSLObj)

        return allLevel
