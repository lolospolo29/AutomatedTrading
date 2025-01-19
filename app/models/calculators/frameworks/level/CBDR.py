import sys

from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class CBDR(ILevel):
    """
     Central Bank Dealer Range 2 PM to 0 AM
     range refers to a predefined high and low level in price.
     The Central Bank Dealers Range, in this context, represents a specific time period during the day
     that holds significance for traders. It serves as a reference point for identifying potential
     deviations in price
     """
    def __init__(self):
        self.name = 'CBDR'

    def return_levels(self, candles: list[Candle]) -> list:
        """Use the Fibonnaci to define the Range"""
        try:
            all_level = []

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

            cbdr_range = high - low

            cbd_range1_bullish_obj = Level(name=self.name, level=low - cbdr_range)
            cbd_range1_bullish_obj.set_fib_level(1, "Bullish", candles=candles)
            cbd_range2_bullish_obj = Level(name=self.name, level=low - cbdr_range - cbdr_range)
            cbd_range2_bullish_obj.set_fib_level(2, "Bullish", candles=candles)
            cbd_range3_bullish_obj = Level(name=self.name, level=low - cbdr_range - cbdr_range - cbdr_range)
            cbd_range3_bullish_obj.set_fib_level(3, "Bullish", candles=candles)

            cbd_range1_bearish_obj = Level(self.name, level=low - cbdr_range)
            cbd_range1_bearish_obj.set_fib_level(1, "Bearish", candles=candles)
            cbd_range2_bearish_obj = Level(self.name, level=low - cbdr_range - cbdr_range)
            cbd_range2_bearish_obj.set_fib_level(2, "Bearish", candles=candles)
            cbd_range3_bearish_obj = Level(self.name, level=low - cbdr_range - cbdr_range - cbdr_range)
            cbd_range3_bearish_obj.set_fib_level(3, "Bearish", candles=candles)

            all_level.append(cbd_range1_bullish_obj)
            all_level.append(cbd_range2_bullish_obj)
            all_level.append(cbd_range3_bullish_obj)

            all_level.append(cbd_range1_bearish_obj)
            all_level.append(cbd_range2_bearish_obj)
            all_level.append(cbd_range3_bearish_obj)

            return all_level
        except Exception as e:
            logger.critical("Exception occurred in CBDR: {}".format(e))
