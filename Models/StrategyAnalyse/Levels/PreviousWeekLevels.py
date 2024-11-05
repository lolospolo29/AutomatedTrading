from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class PreviousWeekLevels(ILevel):
    def getLevels(self, candles: list[Candle]) -> list[Level]:
        allHighs = []
        allLows = []
        allLevel = []

        for dataPoint in candles:  # Using camelCase for the variable
            allHighs.extend(dataPoint.high)
            allLows.extend(dataPoint.low)

        # Step 2: Calculate the overall high and low
        high = max(allHighs) if allHighs else 0  # Added a safeguard for empty lists
        low = min(allLows) if allLows else 0

        PWHObj = Level(name="PWH", level=high)
        PWLObj = Level(name="PWL", level=low)

        allLevel.append(PWHObj)
        allLevel.append(PWLObj)

        return allLevel
