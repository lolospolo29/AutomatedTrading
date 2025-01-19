from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.exceptions.CalculationExceptionError import CalculationExceptionError
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class Breaker(IPDArray):
    """
    An ICT breaker block is basically a failed order block causing a
    shift in market structure and acting as a level
    of support or resistance for the price
    """

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "Breaker"

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        try:
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
                low = low
                high = high
                return (low + high) / 2
        except Exception as e:
            raise CalculationExceptionError("Breaker Entry Error")

    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        return self.return_entry(pd_array, order_direction, risk_mode)

    def return_candle_range(self, pd_array: PDArray) -> tuple[float,float]:
        """
        Returns the Breaker Candle high to low.

        :param pd_array: A PDArray object that contains the candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """
        try:

            # Extract price from the candles
            high = [candle.high for candle in pd_array.candles]
            low = [candle.low for candle in pd_array.candles]

            high = max(high)
            low = min(low)

            return low, high
        except Exception as e:
            raise CalculationExceptionError("Breaker Candle Range Error")

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

    def return_array_list(self, candles: list[Candle]) -> list[PDArray]:
        """
        Calculates Breakers inside a specific Range,which is Calculated by Breaking the Current Structure
        """
        pd_array_list = []

        try:
            if len(candles) < self.lookback:
                return []

            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            # List to store PDArray objects

            # Find swing highs and lows
            swings = self._findSwingPoints(highs, lows)

            # Identify breaker candles
            for swing in swings['highs']:
                swingIdx, swingHigh = swing
                for i in range(swingIdx + 1, len(close)):
                    if close[i] > swingHigh:  # Bullish breaker condition
                        pdArray = PDArray(name=self.name, direction="Bullish")
                        pdArray.candles.append(candles[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                        pd_array_list.append(pdArray)
                        # Store breaker details if needed
                        break  # Stop after the first breaker is found

            for swing in swings['lows']:
                swingIdx, swingLow = swing
                for i in range(swingIdx + 1, len(close)):
                    if close[i] < swingLow:  # Bearish breaker condition
                        pdArray = PDArray(name=self.name, direction="Bearish")
                        pdArray.candles.append(candles[swingIdx])  # Add ID of last candle in the swing (not the one breaking it)
                        pd_array_list.append(pdArray)
                        # Store breaker details if needed
                        break  # Stop after the first breaker is found

        except Exception as e:
            raise logger.error("Breaker Error with Exception"+str(e))
        finally:
            return pd_array_list