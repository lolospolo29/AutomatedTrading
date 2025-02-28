import sys

from app.helper.calculator.framework.level.LevelEnum import LevelEnum
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.interfaces.framework.ILevel import ILevel
from app.monitoring.logging.logging_startup import logger


class PD(ILevel):
    """
       ICT PD arrays are the arrangement of ICT trade entry tools in the premium and discount zone.
       Traders use the PD arrays to find the optimal price for buying and selling in the market.
    """
    def __init__(self):
        self.pd_levels: list[float] = [1.0, 0.5, 0]
        self.name = LevelEnum.PREMIUMDISCOUNT.value

    def return_levels(self, candles: list[Candle], lookback: int = None) -> list[Level]:
        all_level = []

        try:
            # Step 1: Apply lookback to limit the range of candles
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
            if lookback is not None and len(candles) < lookback:
                return []

            # Step 1: Extract high and low values from the data points

            # Step 1: Extract high and low values from the data points
            high = -1
            high_candle = None
            low = sys.maxsize
            low_candle = None

            for candle in candles:
                if high  < candle.high:
                    high = candle.high
                    high_candle = candle
                if low > candle.low:
                    low = candle.low
                    low_candle = candle
            candles:list[Candle] = [high_candle, low_candle]

            # Step 3: Calculate the PD levels
            level0 = low  # 0.0 corresponds to the low value
            level1 = high  # 1.0 corresponds to the high value
            level05 = (high + low) / 2  # 0.5 is the midpoint between high and low

            # Step 4: Create Level objects with names "0.0", "0.5", and "1.0"
            level0_obj = Level(name=self.name, level=level0,direction="Bullish",fib_level=0.0,candles=candles)
            level05_obj = Level(name=self.name, level=level05,direction="EQ",fib_level=0.5,candles=candles)
            level1_obj = Level(name=self.name, level=level1,direction="Bearish",fib_level=1.0,candles=candles)

            all_level.append(level0_obj)
            all_level.append(level05_obj)
            all_level.append(level1_obj)
        except Exception as e:
            logger.error("Projecting the PD failed with exception: {}".format(e))
        finally:
            return all_level
