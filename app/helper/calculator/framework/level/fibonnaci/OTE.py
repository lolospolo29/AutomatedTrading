import sys

from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel
from app.monitoring.logging.logging_startup import logger


class OTE(ILevel):
    """ICT OTE is the retracement level of price based on fibonacci between an established high and low
       , from where price is expected to reverse.
       At the ICT optimal trade entry level,
       the risk is neither too little nor too high and is likely to give you the best return"""
    def __init__(self):
        """
        A class instance for handling the OTE (Optimal Trade Entry) retracement levels.

        The purpose is to calculate Fibonacci retracement levels commonly used in trading
        strategies for identifying optimal trading entries.

        """
        # Fibonacci retracement levels to calculate
        self.retracement_levels: list[float] = [0.79, 0.62,1.5]
        self.name = "OTE"

    def return_levels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        """
        Projects the High and the Low of the given Candles with Lookback
        :param candles:
        :param lookback:
        """
        all_levels = []

        try:
            # Step 1: Apply lookback to limit the range of candles
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
            if lookback is not None and len(candles) < lookback:
                return []

            # Step 1: Extract high and low values from the data points
            high = -1
            high_candle = None
            low = sys.maxsize
            low_candle = None

            # Collecting high and low values from each data point
            for candle in candles:
                if high  < float(candle.high):
                    high = candle.high
                    high_candle = candle
                if low > float(candle.low):
                    low = candle.low
                    low_candle = candle
            candles:list[Candle] = [high_candle, low_candle]

            levels = self._generate_fib_levels_bullish(candles,high,low)
            all_levels.extend(levels)
            levels = self._generate_fib_levels_bearish(candles,high,low)
            all_levels.extend(levels)

        except Exception as e:
            logger.error("Return Levels failed with exception:{e}".format(e=e))
        finally:
            return all_levels

    def _generate_fib_levels_bullish(self, candles: list[Candle],high:float,low:float) -> list[Level]:
        levels = []
        for fib_level in self.retracement_levels:
            bullish_level = high - fib_level * (high - low)
            levels.append(Level(name=self.name, level=bullish_level,fib_level=fib_level,
                                candles=candles,direction="Bullish"))
        return levels

    def _generate_fib_levels_bearish(self, candles: list[Candle],high:float,low:float) -> list[Level]:
        levels = []
        for fib_level in self.retracement_levels:
            bearish_level = low + fib_level  * (high - low)
            levels.append(Level(name=self.name, level=bearish_level,fib_level=fib_level,
                                candles=candles,direction="Bearish"))
        return levels