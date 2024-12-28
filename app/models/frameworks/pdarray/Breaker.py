from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.trade.OrderDirectionEnum import OrderDirection


class Breaker(IPDArray):  # id need to be fixed


    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "Breaker"

    def returnEntry(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode):
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

    def returnStop(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode):
        return self.returnEntry(pdArray, orderDirection, riskMode)

    def returnCandleRange(self, pdArray: PDArray) -> dict:
        """
        Returns the Breaker Candle high to low.

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

    def _findSwingPoints(self, high: list, low: list):
        lookback = self.lookback

        """Find swing highs and lows"""
        swings = {'highs': [], 'lows': []}
        for i in range(lookback, len(high) - lookback):
            if high[i] == max(high[i - lookback:i + lookback + 1]):
                swings['highs'].append((i, high[i]))  # Store index and value of swing high
            if low[i] == min(low[i - lookback:i + lookback + 1]):
                swings['lows'].append((i, low[i]))  # Store index and value of swing low
        return swings

    def returnArrayList(self, candles: list[Candle]) -> list[PDArray]:
        """Get confirmation for breaker blocks"""

        if len(candles) < self.lookback:
            return []

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        # List to store PDArray objects
        pdArrayList = []

        # Find swing highs and lows
        swings = self._findSwingPoints(highs, lows)

        # Identify breaker candles
        for swing in swings['highs']:
            swingIdx, swingHigh = swing
            for i in range(swingIdx + 1, len(close)):
                if close[i] > swingHigh:  # Bullish breaker condition
                    pdArray = PDArray(name=self.name, direction="Bullish")
                    pdArray.addId(ids[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                    pdArrayList.append(pdArray)
                    # Store breaker details if needed
                    break  # Stop after the first breaker is found

        for swing in swings['lows']:
            swingIdx, swingLow = swing
            for i in range(swingIdx + 1, len(close)):
                if close[i] < swingLow:  # Bearish breaker condition
                    pdArray = PDArray(name=self.name, direction="Bearish")
                    pdArray.addId(ids[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                    pdArrayList.append(pdArray)
                    # Store breaker details if needed
                    break  # Stop after the first breaker is found

        return pdArrayList  # Return the list of PDArray objects
