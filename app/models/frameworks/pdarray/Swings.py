from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.trade.OrderDirectionEnum import OrderDirection


class Swings(IPDArray):


    def __init__(self):
        self.name = "Swing"

    def returnEntry(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode):
        pass

    def returnStop(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode) -> float:
        high = [candle.high for candle in pdArray.candles]
        low = [candle.low for candle in pdArray.candles]

        if riskMode == RiskMode.BUY:
            return min (low)
        if riskMode == RiskMode.SELL:
            return max (high)

    def returnCandleRange(self, pdArray: PDArray) -> dict:
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
        swingList = []  # List to store PDArray objects

        if len(candles) < 3:
            return swingList

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        n = len(opens)
        if n > 2:
            # Loop through the data and check 3 consecutive candles for FVGs
            for i in range(2, n):
                open1, high1, low1, close1, id1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2], ids[i - 2]
                open2, high2, low2, close2, id2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1], ids[i - 1]
                open3, high3, low3, close3, id3 = opens[i], highs[i], lows[i], close[i], ids[i]

                if high3 < high2 and high1 < high2:
                    pdArray =PDArray(name="High", direction="Bullish")
                    pdArray.addId(id1)
                    pdArray.addId(id2)
                    pdArray.addId(id3)
                    swingList.append(pdArray)
                if low3 > low2 and low1 > low2:
                    pdArray = PDArray(name="Low", direction="Bearish")
                    pdArray.addId(id1)
                    pdArray.addId(id2)
                    pdArray.addId(id3)
                    swingList.append(pdArray)
        return swingList
