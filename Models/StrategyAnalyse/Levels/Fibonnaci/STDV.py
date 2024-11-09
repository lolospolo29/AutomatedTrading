from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse import PDArray
from Models.StrategyAnalyse.Level import Level


class STDV(ILevel):
    def __init__(self):
        self.extensionLevels: list[float] = [1.5, 2, 3, 4]
        self.name = "STDV"

    def returnLevels(self, candle: Candle, candles: list[Candle], pdArray: PDArray) -> list:
        allLevel = []
        breakerHigh = candle.high
        breakerId = candle.id
        breakerLow = candle.low
        filteredCandles: list = []
        if  pdArray.name == "Breaker" and pdArray.direction == "Bearish":
            # Extract levels from the bearish breaker

            # Step 1: Filter data points lower than the bearish breaker
            for candle in candles:
                if  breakerLow < candle.low:
                    filteredCandles.append(candle)

            if not filteredCandles:
                return allLevel  # No relevant data points

            # Step 2: Calculate Fibonacci levels down to the breaker candle
            high = None
            highId = None
            low = None
            lowId = None

            for candle in candles:
                if high < candle.high:
                    high = candle.high
                    highId = candle.id
                if low > candle.low:
                    low = candle.low
                    lowId = candle.id

            fibLevel15Bearish = high - 1.5 * (high - breakerLow)
            fibLevel20Bearish = high - 2 * (high - breakerLow)
            fibLevel30Bearish = high - 3 * (high - breakerLow)
            fibLevel40Bearish = high - 4 * (high - breakerLow)

            fibLevel15BearishObj = Level(name=self.name, level=fibLevel15Bearish)
            fibLevel15BearishObj.setFibLevel(1.5,"Bearish",[highId,lowId,breakerId])
            fibLevel20BearishObj = Level(name=self.name, level=fibLevel20Bearish)
            fibLevel20BearishObj.setFibLevel(2.5,"Bearish",[highId,lowId,breakerId])
            fibLevel30BearishObj = Level(name=self.name, level=fibLevel30Bearish)
            fibLevel30BearishObj.setFibLevel(3.0,"Bearish",[highId,lowId,breakerId])
            fibLevel40BearishObj = Level(name=self.name, level=fibLevel40Bearish)
            fibLevel40BearishObj.setFibLevel(4.0,"Bearish",[highId,lowId,breakerId])

            allLevel.append(fibLevel15BearishObj)
            allLevel.append(fibLevel20BearishObj)
            allLevel.append(fibLevel30BearishObj)
            allLevel.append(fibLevel40BearishObj)
            return allLevel

        elif pdArray.name == "Breaker" and pdArray.direction == "Bullish":
            # Step 1: Filter data points higher than the bullish breaker
            for candle in candles:
                if breakerLow < candle.low:
                    filteredCandles.append(candle)

            if not filteredCandles:
                return allLevel  # No relevant data points

            # Step 2: Calculate Fibonacci levels up to the breaker candle
            high = None
            highId = None
            low = None
            lowId = None

            for candle in candles:
                if high < candle.high:
                    high = candle.high
                    highId = candle.id
                if low > candle.low:
                    low = candle.low
                    lowId = candle.id

            minLow = min([min(candle.low) for candle in filteredCandles])
            fibLevel15Bullish = minLow + 1.5 * (breakerHigh - minLow)
            fibLevel20Bullish = minLow + 2 * (breakerHigh - minLow)
            fibLevel30Bullish = minLow + 3 * (breakerHigh - minLow)
            fibLevel40Bullish = minLow + 4 * (breakerHigh - minLow)

            fibLevel15BullishObj = Level(self.name, level=fibLevel15Bullish)
            fibLevel15BullishObj.setFibLevel(1.5,"Bullish",[highId,lowId,breakerId])
            fibLevel20BullishObj = Level(self.name, level=fibLevel20Bullish)
            fibLevel20BullishObj.setFibLevel(2.0,"Bullish",[highId,lowId,breakerId])
            fibLevel30BullishObj = Level(self.name, level=fibLevel30Bullish)
            fibLevel30BullishObj.setFibLevel(3.0,"Bullish",[highId,lowId,breakerId])
            fibLevel40BullishObj = Level(self.name, level=fibLevel40Bullish)
            fibLevel40BullishObj.setFibLevel(4.0,"Bullish",[highId,lowId,breakerId])

            allLevel.append(fibLevel15BullishObj)
            allLevel.append(fibLevel20BullishObj)
            allLevel.append(fibLevel30BullishObj)
            allLevel.append(fibLevel40BullishObj)

            return allLevel

        return allLevel  # In case direction is not recognized
