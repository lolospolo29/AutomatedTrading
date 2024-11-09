from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse import PDArray
from Models.StrategyAnalyse.Level import Level


class STDV(ILevel):
    def __init__(self):
        self.extensionLevels: list[float] = [1.5, 2, 3, 4]

    def returnLevels(self, pdArray: PDArray, candles: list[Candle]) -> list:
        allLevel = []
        if pdArray.name == "bearish_breaker":
            # Extract levels from the bearish breaker
            breakerHigh = max(pdArray.high)
            breakerLow = min(pdArray.low)

            # Step 1: Filter data points lower than the bearish breaker
            filteredDataPoints = [dataPoint for dataPoint in candles if min(dataPoint.low) > breakerLow]

            if not filteredDataPoints:
                return None  # No relevant data points

            # Step 2: Calculate Fibonacci levels down to the breaker candle
            maxHigh = max([max(dataPoint.high) for dataPoint in filteredDataPoints])
            fibLevel15Bearish = maxHigh - 1.5 * (maxHigh - breakerLow)
            fibLevel20Bearish = maxHigh - 2 * (maxHigh - breakerLow)
            fibLevel30Bearish = maxHigh - 3 * (maxHigh - breakerLow)
            fibLevel40Bearish = maxHigh - 4 * (maxHigh - breakerLow)

            fibLevel15BearishObj = Level(name="stdv_1.5_bearish", level=fibLevel15Bearish)
            fibLevel20BearishObj = Level(name="stdv_2.0_bearish", level=fibLevel20Bearish)
            fibLevel30BearishObj = Level(name="stdv_3.0_bearish", level=fibLevel30Bearish)
            fibLevel40BearishObj = Level(name="stdv_4.0_bearish", level=fibLevel40Bearish)

            allLevel.append(fibLevel15BearishObj)
            allLevel.append(fibLevel20BearishObj)
            allLevel.append(fibLevel30BearishObj)
            allLevel.append(fibLevel40BearishObj)
            return allLevel

        elif pdArray.name == "bullish_breaker":
            # Extract levels from the bullish breaker
            breakerLow = min(pdArray.low)
            breakerHigh = max(pdArray.high)

            # Step 1: Filter data points higher than the bullish breaker
            filteredDataPoints = [dataPoint for dataPoint in candles if max(dataPoint.high) < breakerHigh]

            if not filteredDataPoints:
                return None  # No relevant data points

            # Step 2: Calculate Fibonacci levels up to the breaker candle
            minLow = min([min(dataPoint.low) for dataPoint in filteredDataPoints])
            fibLevel15Bullish = minLow + 1.5 * (breakerHigh - minLow)
            fibLevel20Bullish = minLow + 2 * (breakerHigh - minLow)
            fibLevel30Bullish = minLow + 3 * (breakerHigh - minLow)
            fibLevel40Bullish = minLow + 4 * (breakerHigh - minLow)

            fibLevel15BullishObj = Level(name="stdv_1.5_bullish", level=fibLevel15Bullish)
            fibLevel20BullishObj = Level(name="stdv_2.0_bullish", level=fibLevel20Bullish)
            fibLevel30BullishObj = Level(name="stdv_3.0_bullish", level=fibLevel30Bullish)
            fibLevel40BullishObj = Level(name="stdv_4.0_bullish", level=fibLevel40Bullish)

            allLevel.append(fibLevel15BullishObj)
            allLevel.append(fibLevel20BullishObj)
            allLevel.append(fibLevel30BullishObj)
            allLevel.append(fibLevel40BullishObj)

            return allLevel

        return allLevel  # In case direction is not recognized
