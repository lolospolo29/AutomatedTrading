from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


class Orderblock(IPDArray):
    def __init__(self):
        self.name: str = "OB"

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


    def checkForInverse(self, pdArray: PDArray, candles: list[Candle]) -> str:

        # Extract the two IDs from the PDArray
        _ids = [candle.id for candle in pdArray.candles]

        # Find the indices of these two IDs in the list of candles
        index1 = next((i for i, c in enumerate(candles) if c.id == _ids[0]), None)
        index2 = next((i for i, c in enumerate(candles) if c.id == _ids[1]), None)

        if index1 is None or index2 is None:
            raise ValueError("One or both IDs from PDArray not found in the candle list.")

        # Determine the older index (the one with the higher value)
        older_index = min(index1, index2)

        start_index = older_index + 1

        # Extract and return the candles
        neighbors = candles[start_index:]

        if len(neighbors) > 0:
            for candle in neighbors:
                low,high = self.returnCandleRange(pdArray)
                if pdArray.direction == "Bullish":
                    if candle.close < low:
                        return "Bearish"
                if pdArray.direction == "Bearish":
                    if candle.close > high:
                        return "Bullish"
        return pdArray.direction

    def returnCandleRange(self, pdArray: PDArray) -> tuple[float, float]:
        """
        Returns the high and low of the OB.

        :param pdArray: A PDArray object that contains candles.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]

        high = max(highs)
        low = min(lows)

        return low,high

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

        if lookback is not None and len(candles) < lookback:
            return []

        if len(candles) < 2:
            return []

        pdArrays = []

        # Extract data points
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]

        n = len(highs)

        # Loop through the data and check 3 consecutive candles for FVGs
        for i in range(1, n):  # Start bei der 2. Kerze (Index 1)
            open1, high1, low1, close1 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1]
            open2, high2, low2, close2 = opens[i], highs[i], lows[i], close[i]

            if close1 < open1 and close2 > open2 and low1 > low2:
                pdArray = PDArray(name="OB",direction="Bullish")
                pdArray.candles.append(candles[i])
                pdArray.candles.append(candles[i-1])
                pdArrays.append(pdArray)
            if close1 > open1 and close2 < open2 and high1 < high2:
                pdArray = PDArray(name="OB",direction="Bearish")
                pdArray.candles.append(candles[i])
                pdArray.candles.append(candles[i-1])
                pdArrays.append(pdArray)
        return pdArrays