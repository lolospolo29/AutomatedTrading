from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class RejectionBlock(IPDArray):
    def __init__(self):
        self.name = "RB"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        rejectionBlocks = None

        # We assume 'data_points_asset' contains the asset data (high, low, open, close, ids)
        opens = candles.open
        highs = candles.high
        lows = candles.low
        closes = candles.close

        if len(opens) < 10:
            return rejectionBlocks  # Not enough data for rejection block detection

        for i in range(9, len(opens)):  # Start from the 10th candle onwards
            # Calculate average range of the previous 10 candles
            avgRange = sum([highs[j] - lows[j] for j in range(i - 9, i + 1)]) / 10

            # Current candle details
            openPrice = opens[i]
            highPrice = highs[i]
            lowPrice = lows[i]
            closePrice = closes[i]

            # Candle type: Bullish or Bearish
            isBullish = closePrice > openPrice
            isBearish = closePrice < openPrice

            # Calculate the wicks
            upperWick = highPrice - max(openPrice, closePrice)
            lowerWick = min(openPrice, closePrice) - lowPrice

            # Bullish rejection: Large lower wick compared to average range
            if isBullish and lowerWick > avgRange:
                rejectionBlocks = PDArray(self.name, "Bullish")
                rejectionBlocks.addId(candles.id[i])
            # Bearish rejection: Large upper wick compared to average range
            elif isBearish and upperWick > avgRange:
                rejectionBlocks = PDArray(self.name, "Bearish")
                rejectionBlocks.addId(candles.id[i])

        return rejectionBlocks
