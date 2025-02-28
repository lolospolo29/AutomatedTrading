from app.helper.calculator.framework.pdarray.PDEnum import PDEnum
from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.frameworks.PDArray import PDArray
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class Swings(IPDArray):
    """Determines a Swing by 3 Candles"""


    def __init__(self):
        self.name = PDEnum.SWINGS.value

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        pass

    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        try:
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
        except Exception as ex:
            logger.error("Swing Stop Error with Exception {}".format(ex))

    def return_candle_range(self, pd_array: PDArray) -> tuple[float,float]:
        """
        Returns the high and low of the Swing

        :param pd_array: A PDArray object that contains the candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """
        try:
            # Extract price from the candles
            high = [candle.high for candle in pd_array.candles]
            low = [candle.low for candle in pd_array.candles]

            high = max(high)
            low = min(low)

            return low,high
        except Exception as e:
            logger.error("Swing Candle Range Error with Exception {}".format(e))

    def return_array_list(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        swing_list = []  # List to store PDArray objects

        try:
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

            if lookback is not None and len(candles) < lookback:
                return []

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
                        pd_array =PDArray(name="High", direction="Bullish",candles=[candles[i],candles[i-1],candles[i-2]])
                        swing_list.append(pd_array)
                    if low3 > low2 and low1 > low2:
                        pd_array = PDArray(name="Low", direction="Bearish",candles=[candles[i],candles[i-1],candles[i-2]])
                        swing_list.append(pd_array)
        except Exception as e:
            logger.error("Swings Calculation failed with exception {}".format(e))
        finally:
            return swing_list
