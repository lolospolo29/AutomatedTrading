from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.monitoring.logging.logging_startup import logger


class Breaker:

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
                logger.exception("Breaker Candle Range Error with Exception"+str(e))
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

    def return_pd_arrays(self, candles: list[Candle]) -> list[PDArray]:
        """
        Calculates Breakers inside a specific Range,which is Calculated by Breaking the Current Structure
        """
        pd_array_list = []

        last_candle:Candle  = candles[-1]

        try:
            if len(candles) < self.lookback:
                return []

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
                        pdArray = PDArray(name=self.name, direction="Bullish",candles=[candles[swingIdx]],timeframe=last_candle.timeframe)
                        pd_array_list.append(pdArray)
                        # Store breaker details if needed
                        break  # Stop after the first breaker is found

            for swing in swings['lows']:
                swingIdx, swingLow = swing
                for i in range(swingIdx + 1, len(close)):
                    if close[i] < swingLow:  # Bearish breaker condition
                        pdArray = PDArray(name=self.name, direction="Bearish",candles=[candles[swingIdx]],timeframe=last_candle.timeframe)
                        pd_array_list.append(pdArray)
                        # Store breaker details if needed
                        break  # Stop after the first breaker is found

        except Exception as e:
            raise logger.error("Breaker Error with Exception"+str(e))
        finally:
            return pd_array_list