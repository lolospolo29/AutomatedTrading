from Core.Main.Asset.SubModels import Candle
from Core.Main.Strategy.FrameWorks.PDArray import PDArray
from Interfaces.Strategy.IPDArray import IPDArray


class Breaker(IPDArray):  # id need to be fixed

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "Breaker"

    def returnCandleRange(self, pdArray: PDArray) -> dict:
        """
        Returns the Breaker Candle high to low.

        :param pdArray: A PDArray object that contains the candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """

        # Extract price from the candles
        high = [candle.high for candle in pdArray.candles]
        low = [candle.low for candle in pdArray.candles]

        high = max(high)
        low = min(low)

        return {
            'low': low,
            'high': high
        }

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

        if len(candles) < self.lookback:
            return []

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
