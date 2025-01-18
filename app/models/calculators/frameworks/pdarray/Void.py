from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class Void(IPDArray):


    def __init__(self):
        self.name = "Void"

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        low,high =self.return_candle_range(pd_array)
        if order_direction.BUY:
            if risk_mode.SAFE:
                return low
            if risk_mode.AGGRESSIVE:
                return high

        if order_direction.SELL:
            if risk_mode.SAFE:
                return high
            if risk_mode.AGGRESSIVE:
                return low

        if risk_mode.MODERAT:
            return (low + high) / 2

    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        highs = [candle.high for candle in pd_array.candles]
        lows = [candle.low for candle in pd_array.candles]
        close =  [candle.close for candle in pd_array.candles]
        open = [candle.open for candle in pd_array.candles]

        if order_direction.BUY:
            if risk_mode.SAFE:
                return min(lows)
            if risk_mode.MODERAT:
                return min(open)
            if risk_mode.AGGRESSIVE:
                return min(close)
        if order_direction.SELL:
            if risk_mode.SAFE:
                return max(highs)
            if risk_mode.MODERAT:
                return max(open)
            if risk_mode.AGGRESSIVE:
                return max(close)

    def return_candle_range(self, pd_array: PDArray) -> tuple[float, float]:
        """
        Returns the high and low of the Gap.

        :param pd_array: A PDArray object that contains the IDs of the six candles forming the BPR.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pd_array.candles]
        lows = [candle.low for candle in pd_array.candles]

        high = max(lows)
        low = min(highs)

        # Return the gap range
        return low,high

    def return_array_list(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:

        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
        if lookback is not None and len(candles) < lookback:
            return []
        pd_arrays = []  # List to store PDArray instances

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]

        for i in range(1, len(close)):
            # Check for a bullish void (upward gap)
            if lows[i] > highs[i - 1]:
                pd_array = PDArray(name=self.name, direction="Bullish")
                pd_array.candles.append(candles[i])
                pd_array.candles.append(candles[i - 1])
                pd_arrays.append(pd_array)

            # Check for a bearish void (downward gap)
            elif highs[i] < lows[i - 1]:
                pd_array = PDArray(name=self.name, direction="Bearish")
                pd_array.candles.append(candles[i])
                pd_array.candles.append(candles[i - 1])
                pd_arrays.append(pd_array)

        return pd_arrays  # Return the list of voids found
