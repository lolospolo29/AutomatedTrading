import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel
from app.monitoring.logging.logging_startup import logger


class OTE(ILevel):
    """Standard OTE Fibonnaci Levels"""
    def __init__(self):
        # Fibonacci retracement levels to calculate
        self.retracement_levels: list[float] = [0.75, 0.62]
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
                if high  < candle.high:
                    high = candle.high
                    high_candle = candle
                if low > candle.low:
                    low = candle.low
                    low_candle = candle


            candles:list[Candle] = [high_candle, low_candle]

            # Step 3: Calculate Bearish Fibonacci retracement levels (from high to low)
            level075_bullish = high - 0.75 * (high - low)
            level062_bullish = high - 0.62 * (high - low)

            # Step 4: Calculate Bullish Fibonacci retracement levels (from low to high)
            level075_bearish = low + 0.75 * (high - low)
            level062_bearish = low + 0.62 * (high - low)

            # Step 5: Create Level objects for each Fibonacci level with bullish/bearish names
            level075_bearish_obj = Level(name=self.name, level=level075_bearish)
            level075_bearish_obj.set_fib_level(0.75, "Bearish", candles)
            level062_bearish_obj = Level(name=self.name, level=level062_bearish)
            level062_bearish_obj.set_fib_level(0.62, "Bearish", candles)
            level075_bullish_obj = Level(name=self.name, level=level075_bullish)
            level075_bullish_obj.set_fib_level(0.75, "Bullish", candles)
            level062_bullish_obj = Level(name=self.name, level=level062_bullish)
            level062_bullish_obj.set_fib_level(0.62, "Bullish", candles)

            all_levels.append(level075_bearish_obj)
            all_levels.append(level062_bearish_obj)
            all_levels.append(level075_bullish_obj)
            all_levels.append(level062_bullish_obj)
        except Exception as e:
            logger.error("Projecting of Fibonnaci Levels failed")
        finally:
            return all_levels
