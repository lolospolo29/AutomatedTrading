from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Orderblock(IPDArray):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name: str = "OB"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:

        if len(candles) < self.lookback:
            return []

        pdArrays = []

        # Extract data points
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        n = len(highs)

        lastBullish = None
        lastBearish = None

        for i in range(self.lookback, n):
            swingHigh = self.getSwingHigh(highs, i, self.lookback)
            swingLow = self.getSwingLow(lows, i, self.lookback)

            # Detect Bullish Order Blocks
            if close[i] > swingHigh and (lastBullish is None or lastBullish['top'] < swingHigh):
                lastBullish = {'top': swingHigh, 'bottom': swingLow}
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(ids[i])
                pdArrays.append(pdArray)

            # Detect Bearish Order Blocks
            if close[i] < swingLow and (lastBearish is None or lastBearish['bottom'] > swingLow):
                lastBearish = {'top': swingHigh, 'bottom': swingLow}
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.addId(ids[i])
                pdArrays.append(pdArray)

        # Return order blocks as PDArray
        return pdArrays

    @staticmethod
    def getSwingHigh(highs: list, currentIndex: int, lookback: int):
        """Returns the highest high within the lookback period."""
        return max(highs[currentIndex - lookback: currentIndex])

    @staticmethod
    def getSwingLow(lows: list, currentIndex: int, lookback: int):
        """Returns the lowest low within the lookback period."""
        return min(lows[currentIndex - lookback: currentIndex])
