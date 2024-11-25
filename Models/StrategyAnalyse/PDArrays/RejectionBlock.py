from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class RejectionBlock(IPDArray):
    def __init__(self, lookback):
        self.lookback = lookback
        self.name = "RB"


    def returnCandleRange(self, pdArray: PDArray) -> dict:
        """
        Returns the high and low of the RB Whick.

        :param pdArray: A PDArray object that contains candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]
        opens = [candle.open for candle in pdArray.candles]
        closes = [candle.close for candle in pdArray.candles]

        if pdArray.direction == "Bullish":
            low = min(lows)
            high = min(opens, closes)
            return {
                'low': low,
                'high': high
            }
        if pdArray.direction == "Bearish":
            low = min(lows)
            high = max(opens, closes)
            return {
                'low': low,
                'high': high
            }

    def returnArrayList(self, candles: list[Candle]) -> list:

        if len(candles) < self.lookback:
            return []

        rejectionBlocks = []

        # We assume 'data_points_asset' contains the asset data (high, low, open, close, ids)
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        if len(opens) < self.lookback:
            return rejectionBlocks  # Not enough data for rejection block detection

        for i in range(9, len(opens)):  # Start from the 10th candle onwards
            # Calculate average range of the previous 10 candles
            avgRange = sum([highs[j] - lows[j] for j in range(i - 9, i + 1)]) / 10

            # Current candle details
            openPrice = opens[i]
            highPrice = highs[i]
            lowPrice = lows[i]
            closePrice = close[i]

            # Calculate the wicks
            upperWick = highPrice - max(openPrice, closePrice)
            lowerWick = min(openPrice, closePrice) - lowPrice

            # Bullish rejection: Large lower wick compared to average range
            if  lowerWick > avgRange:
                rejectionBlocks = PDArray(self.name, "Bullish")
                rejectionBlocks.addId(ids[i])
            # Bearish rejection: Large upper wick compared to average range
            elif upperWick > avgRange:
                rejectionBlocks = PDArray(self.name, "Bearish")
                rejectionBlocks.addId(ids[i])

        return rejectionBlocks
