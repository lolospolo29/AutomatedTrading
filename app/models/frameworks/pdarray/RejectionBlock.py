from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.trade.OrderDirectionEnum import OrderDirection


class RejectionBlock(IPDArray):

    def __init__(self, lookback):
        self.lookback = lookback
        self.name = "RB"

    def returnEntry(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode) -> float:
        range = self.returnCandleRange(pdArray)
        if orderDirection.BUY:
            if riskMode.AGGRESSIVE:
                return range.get("high")

        if orderDirection.SELL:
            if riskMode.AGGRESSIVE:
                return range.get("low")

        if riskMode.MODERAT or riskMode.SAFE:
            low = range.get("low")
            high = range.get("high")
            return (low + high) / 2

    def returnStop(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode):
        range = self.returnCandleRange(pdArray)
        if orderDirection.BUY:
            if riskMode.SAFE:
                return range.get("low")

        if orderDirection.SELL:
            if riskMode.SAFE:
                return range.get("high")

        if riskMode.MODERAT or riskMode.AGGRESSIVE:
            low = range.get("low")
            high = range.get("high")
            return (low + high) / 2

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
            high = min(opens,closes)
            return {
                'low': low,
                'high': high
            }
        if pdArray.direction == "Bearish":
            low = max(opens,closes)
            high = max(highs)
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
