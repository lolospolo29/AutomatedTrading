import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel


class STDV(ILevel):
    def __init__(self):
        self.extension_levels: list[float] = [1.5, 2, 3, 4]
        self.name = "STDV"

    def return_levels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        # Step 1: Apply lookback to limit the range of candles
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

            candles:list[Candle] = [high_candle, low_candle]

            fib_level15_bullish = high - 1.5 * (high - low)
            fib_level20_bullish = high - 2 * (high - low)
            fib_level30_bullish = high - 3 * (high - low)
            fib_level40_bullish = high - 4 * (high - low)

            fib_level15_bearish = low + 1.5 * (high - low)
            fib_level20_bearish = low + 2 * (high - low)
            fib_level30_bearish = low + 3 * (high - low)
            fib_level40_bearish = low + 4 * (high - low)

            fib_level15_bearish_obj = Level(name=self.name, level=fib_level15_bearish)
            fib_level15_bearish_obj.set_fib_level(1.5, "Bearish", candles=candles)
            fib_level20_bearish_obj = Level(name=self.name, level=fib_level20_bearish)
            fib_level20_bearish_obj.set_fib_level(2.5, "Bearish", candles=candles)
            fib_level30_bearish_obj = Level(name=self.name, level=fib_level30_bearish)
            fib_level30_bearish_obj.set_fib_level(3.0, "Bearish", candles=candles)
            fib_level40_bearish_obj = Level(name=self.name, level=fib_level40_bearish)
            fib_level40_bearish_obj.set_fib_level(4.0, "Bearish", candles=candles)

            all_level.append(fib_level15_bearish_obj)
            all_level.append(fib_level20_bearish_obj)
            all_level.append(fib_level30_bearish_obj)
            all_level.append(fib_level40_bearish_obj)

            fib_level15_bullish_obj = Level(self.name, level=fib_level15_bullish)
            fib_level15_bullish_obj.set_fib_level(1.5, "Bullish", candles=candles)
            fib_level20_bullish_obj = Level(self.name, level=fib_level20_bullish)
            fib_level20_bullish_obj.set_fib_level(2.0, "Bullish", candles=candles)
            fib_level30_bullish_obj = Level(self.name, level=fib_level30_bullish)
            fib_level30_bullish_obj.set_fib_level(3.0, "Bullish", candles=candles)
            fib_level40_bullish_obj = Level(self.name, level=fib_level40_bullish)
            fib_level40_bullish_obj.set_fib_level(4.0, "Bullish", candles=candles)

            all_level.append(fib_level15_bullish_obj)
            all_level.append(fib_level20_bullish_obj)
            all_level.append(fib_level30_bullish_obj)
            all_level.append(fib_level40_bullish_obj)

            return all_level