from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class Swings(IPDArray):


    def __init__(self):
        self.name = "Swing"

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        pass

    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        high = [candle.high for candle in pd_array.candles]
        low = [candle.low for candle in pd_array.candles]
        if order_direction == OrderDirectionEnum.BUY:
            if risk_mode == RiskMode.SAFE:
                return min (low)
            if risk_mode == RiskMode.AGGRESSIVE:
                return max (high)
        if order_direction == OrderDirectionEnum.SELL:
            if risk_mode == RiskMode.SAFE:
                return max (high)
            if risk_mode == RiskMode.AGGRESSIVE:
                return min (low)

    def return_candle_range(self, pd_array: PDArray) -> tuple[float,float]:
        """
        Returns the high and low of the Swing

        :param pd_array: A PDArray object that contains the candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """

        # Extract price from the candles
        high = [candle.high for candle in pd_array.candles]
        low = [candle.low for candle in pd_array.candles]

        high = max(high)
        low = min(low)

        return low,high

    def return_array_list(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

        if lookback is not None and len(candles) < lookback:
            return []
        swing_list = []  # List to store PDArray objects

        if len(candles) < 3:
            return swing_list

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
                    pd_array =PDArray(name="High", direction="Bullish")
                    pd_array.candles.append(candles[i])
                    pd_array.candles.append(candles[i-1])
                    pd_array.candles.append(candles[i-2])
                    swing_list.append(pd_array)
                if low3 > low2 and low1 > low2:
                    pd_array = PDArray(name="Low", direction="Bearish")
                    pd_array.candles.append(candles[i])
                    pd_array.candles.append(candles[i-1])
                    pd_array.candles.append(candles[i-2])
                    swing_list.append(pd_array)
        return swing_list
