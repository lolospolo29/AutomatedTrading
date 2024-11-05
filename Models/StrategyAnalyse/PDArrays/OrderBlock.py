from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Orderblock(IPDArray):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name: str = "OB"

    def getCandleRange(self, candles: list[Candle]):
        pass

    def getArrayList(self, candles: list[Candle]) -> list[PDArray]:
        lookback = self.lookback

        pdArrays = []

        # Extract data points
        highs = candles.high
        lows = candles.low
        closes = candles.close
        ids = candles.id

        n = len(highs)

        lastBullish = None
        lastBearish = None

        for i in range(lookback, n):
            swingHigh = self.getSwingHigh(highs, i, lookback)
            swingLow = self.getSwingLow(lows, i, lookback)

            # Detect Bullish Order Blocks
            if closes[i] > swingHigh and (lastBullish is None or lastBullish['top'] < swingHigh):
                lastBullish = {'top': swingHigh, 'bottom': swingLow}
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(ids[i])
                pdArrays.append(pdArray)

            # Detect Bearish Order Blocks
            if closes[i] < swingLow and (lastBearish is None or lastBearish['bottom'] > swingLow):
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
