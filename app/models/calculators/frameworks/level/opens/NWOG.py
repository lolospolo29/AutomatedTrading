import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class NWOG:

    def __init__(self):
        self.name = 'NWOG'

    def return_levels(self, candles:list[Candle]) -> list[Level]:
        all_levels = []
        try:
            for candle in candles:
                # Check if the candle time is at UTC-5 midnight
                if candle.iso_time.hour == 0 and candle.iso_time.minute == 0 and candle.iso_time.weekday() == 0:

                    nwog = Level(self.name, level=candle.open)
                    nwog.set_fib_level(0.0, "NWOG", candles=[candle])

                    all_levels.append(nwog)
                    # Add high and low of the New York midnight candle to levels
        except Exception as e:
            logger.critical("NWOG Calculation Error")
        finally:
            return all_levels
