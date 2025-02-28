import sys

from app.helper.calculator.framework.level.LevelEnum import LevelEnum
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel
from app.monitoring.logging.logging_startup import logger


class STDV(ILevel):
    """
    Standard deviations are a statistical measure that helps traders understand the variability of price movements
    """

    def __init__(self):
        self.extension_levels: list[float] = [1.5, 2, 3, 4]
        self.name = LevelEnum.STANDARDDIVIATION.value

    def return_levels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        # Step 1: Apply lookback to limit the range of candles
        try:
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
            if lookback is not None and len(candles) < lookback:
                return []

            all_level = []

            # Step 2: Calculate Fibonacci levels down to the breaker candle
            high = -1
            high_candle = None
            low = sys.maxsize
            low_candle = None

            # Collecting high and low values from each data point
            for candle in candles:
                if high < candle.high:
                    high = candle.high
                    high_candle = candle
                if low > candle.low:
                    low = candle.low
                    low_candle = candle

            candles: list[Candle] = [high_candle, low_candle]

            levels = self._generate_fib_levels_bullish(candles, high, low)
            all_level.extend(levels)
            levels = self._generate_fib_levels_bearish(candles, high, low)
            all_level.extend(levels)

            return all_level
        except Exception as e:
            logger.error("STDV Calculation failed with exception {}".format(e))

    def _generate_fib_levels_bullish(self, candles: list[Candle], high: float, low: float) -> list[Level]:
        levels = []
        last_candle:Candle = candles[-1]
        for fib_level in self.extension_levels:
            bullish_level = high - fib_level * (high - low)
            levels.append(Level(name=self.name, level=bullish_level, fib_level=fib_level,
                                candles=candles, direction="Bullish",timeframe=last_candle.timeframe))
        return levels

    def _generate_fib_levels_bearish(self, candles: list[Candle], high: float, low: float) -> list[Level]:
        levels = []
        last_candle:Candle = candles[-1]
        for fib_level in self.extension_levels:
            bearish_level = low + fib_level * (high - low)
            levels.append(Level(name=self.name, level=bearish_level, fib_level=fib_level,
                                candles=candles, direction="Bearish",timeframe=last_candle.timeframe))
        return levels
