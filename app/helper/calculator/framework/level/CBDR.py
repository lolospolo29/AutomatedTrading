import sys

from app.helper.calculator.framework.level.LevelEnum import LevelEnum
from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
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
        self.name = LevelEnum.CENTRALBANKDEALERRANGE.value
        self.projection_width = 3

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

            cbdr_range_obj = Level(name=self.name, level=low - cbdr_range,fib_level=cbdr_range, candles=candles,direction="")
            all_level.append(cbdr_range_obj)

            return all_level
        except Exception as e:
            logger.critical("Exception occurred in CBDR: {}".format(e))
