from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


class Swings(IPDArray):


    def __init__(self):
        self.name = "Swing"

    def returnEntry(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode):
        pass

    def returnStop(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode) -> float:
        high = [candle.high for candle in pdArray.candles]
        low = [candle.low for candle in pdArray.candles]
        if orderDirection == OrderDirection.BUY:
            if riskMode == RiskMode.SAFE:
                return min (low)
            if riskMode == RiskMode.AGGRESSIVE:
                return max (high)
        if orderDirection == OrderDirection.SELL:
            if riskMode == RiskMode.SAFE:
                return max (high)
            if riskMode == RiskMode.AGGRESSIVE:
                return min (low)

    def returnCandleRange(self, pdArray: PDArray) -> tuple[float,float]:
        """
        Returns the high and low of the Swing

        :param pdArray: A PDArray object that contains the candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """

        # Extract price from the candles
        high = [candle.high for candle in pdArray.candles]
        low = [candle.low for candle in pdArray.candles]

        high = max(high)
        low = min(low)

        return low,high

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

        if lookback is not None and len(candles) < lookback:
            return []
        swingList = []  # List to store PDArray objects

        if len(candles) < 3:
            return swingList

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]

        n = len(opens)
        if n > 2:
            # Loop through the data and check 3 consecutive candles for FVGs
            for i in range(2, n):
                open1, high1, low1, close1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2]
                open2, high2, low2, close2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1]
                open3, high3, low3, close3 = opens[i], highs[i], lows[i], close[i]

                if high3 < high2 and high1 < high2:
                    pdArray =PDArray(name="High", direction="Bullish")
                    pdArray.candles.append(candles[i])
                    pdArray.candles.append(candles[i-1])
                    pdArray.candles.append(candles[i-2])
                    swingList.append(pdArray)
                if low3 > low2 and low1 > low2:
                    pdArray = PDArray(name="Low", direction="Bearish")
                    pdArray.candles.append(candles[i])
                    pdArray.candles.append(candles[i-1])
                    pdArray.candles.append(candles[i-2])
                    swingList.append(pdArray)
        return swingList
