from Interfaces.Strategy.ILevel import ILevel
from Models.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class CBDR(ILevel):
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

        cbdrRange = high - low

        cbdRange1BullishObj = Level(name="cbdr_1_bullish", level=low - cbdrRange)
        cbdRange2BullishObj = Level(name="cbdr_2_bullish", level=low - cbdrRange - cbdrRange)
        cbdRange3BullishObj = Level(name="cbdr_3_bullish", level=low - cbdrRange - cbdrRange - cbdrRange)

        cbdRange1BearishObj = Level(name="cbdr_1_bearish", level=low - cbdrRange)
        cbdRange2BearishObj = Level(name="cbdr_2_bearish", level=low - cbdrRange - cbdrRange)
        cbdRange3BearishObj = Level(name="cbdr_3_bearish", level=low - cbdrRange - cbdrRange - cbdrRange)

        allLevel.append(cbdRange1BullishObj)
        allLevel.append(cbdRange2BullishObj)
        allLevel.append(cbdRange3BullishObj)

        allLevel.append(cbdRange1BearishObj)
        allLevel.append(cbdRange2BearishObj)
        allLevel.append(cbdRange3BearishObj)

        return allLevel
