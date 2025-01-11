from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


class Void(IPDArray):


    def __init__(self):
        self.name = "Void"

    def returnEntry(self,pdArray: PDArray,orderDirection: OrderDirection,riskMode: RiskMode) -> float:
        low,high =self.returnCandleRange(pdArray)
        if orderDirection.BUY:
            if riskMode.SAFE:
                return low
            if riskMode.AGGRESSIVE:
                return high

        if orderDirection.SELL:
            if riskMode.SAFE:
                return high
            if riskMode.AGGRESSIVE:
                return low

        if riskMode.MODERAT:
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

    def returnCandleRange(self, pdArray: PDArray) -> tuple[float, float]:
        """
        Returns the high and low of the Gap.

        :param pdArray: A PDArray object that contains the IDs of the six candles forming the BPR.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]

        high = max(lows)
        low = min(highs)

        # Return the gap range
        return low,high

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

        for i in range(1, len(close)):
            # Check for a bullish void (upward gap)
            if lows[i] > highs[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.candles.append(candles[i])
                pdArray.candles.append(candles[i - 1])
                pdArrays.append(pdArray)

            # Check for a bearish void (downward gap)
            elif highs[i] < lows[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.candles.append(candles[i])
                pdArray.candles.append(candles[i - 1])
                pdArrays.append(pdArray)

        return pdArrays  # Return the list of voids found
