from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.trade.OrderDirectionEnum import OrderDirection


class VolumeImbalance(IPDArray):

    def __init__(self):
        self.name = "VI"

    def returnEntry(self,pdArray: PDArray,orderDirection: OrderDirection,riskMode: RiskMode) -> float:
        range =self.returnCandleRange(pdArray)
        if orderDirection.BUY:
            if riskMode.SAFE:
                return range.get("low")
            if riskMode.AGGRESSIVE:
                return range.get("high")

        if orderDirection.SELL:
            if riskMode.SAFE:
                return range.get("high")
            if riskMode.AGGRESSIVE:
                return range.get("low")

        if riskMode.MODERAT:
            low = range.get("low")
            high = range.get("high")
            return (low + high) / 2

    def returnStop(self,pdArray: PDArray,orderDirection: OrderDirection,riskMode: RiskMode) -> float:
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]
        close =  [candle.close for candle in pdArray.candles]
        open = [candle.open for candle in pdArray.candles]

        if orderDirection.BUY:
            if riskMode.SAFE:
                return min(lows)
            if riskMode.MODERAT:
                return min(open)
            if riskMode.AGGRESSIVE:
                return min(close)
        if orderDirection.SELL:
            if riskMode.SAFE:
                return max(highs)
            if riskMode.MODERAT:
                return max(open)
            if riskMode.AGGRESSIVE:
                return max(close)

    def returnCandleRange(self, pdArray: PDArray) -> dict:
        """
        Returns the gap between two Fair Value Gaps (FVGs) within the Balanced Price Range (BPR).

        :param pdArray: A PDArray object that contains the IDs of the six candles forming the BPR.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]

        high = max(lows)
        low = min(highs)

        # Return the gap range
        return {
            'low': low,
            'high': high
        }

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
        if lookback is not None and len(candles) < lookback:
            return []
        pdArrays = []  # List to store PDArray instances

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        for i in range(1, len(close)):
            # Check for a bullish vi
            if min(opens[i], close[i]) > highs[i - 1] and \
                    lows[i] > max(opens[i - 1], close[-1]) and \
                    (lows[i] <= highs[i - 1]):
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(ids[i])
                pdArray.addId(ids[i - 1])
                pdArrays.append(pdArray)

            # Check for a bearish vi
            elif max(opens[i], close[i]) < lows[i - 1] and \
                    highs[i] < min(opens[i - 1], close[-1]) and \
                    (highs[i] >= lows[i - 1]):
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.addId(ids[i])
                pdArray.addId(ids[i - 1])
                pdArrays.append(pdArray)

        return pdArrays  # Return the list of voids found
