from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Breaker(IPDArray):  # id need to be fixed

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "Breaker"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def findSwingPoints(self, high: list, low: list):
        lookback = self.lookback

        """Find swing highs and lows"""
        swings = {'highs': [], 'lows': []}
        for i in range(lookback, len(high) - lookback):
            if high[i] == max(high[i - lookback:i + lookback + 1]):
                swings['highs'].append((i, high[i]))  # Store index and value of swing high
            if low[i] == min(low[i - lookback:i + lookback + 1]):
                swings['lows'].append((i, low[i]))  # Store index and value of swing low
        return swings

    def returnArrayList(self, candles: list[Candle]) -> list:
        """Get confirmation for breaker blocks"""
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        # List to store PDArray objects
        pdArrayList = []

        # Find swing highs and lows
        swings = self.findSwingPoints(highs, lows)

        # Identify breaker candles
        for swing in swings['highs']:
            swingIdx, swingHigh = swing
            for i in range(swingIdx + 1, len(close)):
                if close[i] > swingHigh:  # Bullish breaker condition
                    pdArray = PDArray(name=self.name, direction="Bullish")
                    pdArray.addId(ids[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                    pdArrayList.append(pdArray)
                    # Store breaker details if needed
                    break  # Stop after the first breaker is found

        for swing in swings['lows']:
            swingIdx, swingLow = swing
            for i in range(swingIdx + 1, len(close)):
                if close[i] < swingLow:  # Bearish breaker condition
                    pdArray = PDArray(name=self.name, direction="Bearish")
                    pdArray.addId(ids[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                    pdArrayList.append(pdArray)
                    # Store breaker details if needed
                    break  # Stop after the first breaker is found

        return pdArrayList  # Return the list of PDArray objects
