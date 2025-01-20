import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class NDOG:
    """ The NDOG is the gap between the opening price and closing price of the previous day"""
    def __init__(self):
        self.name = 'NDOG'

    def return_levels(self, candles: list[Candle]) -> list[Level]:
        all_levels = []
        try:
            logger.info("Calculating NDOG levels...")
            for candle in candles:
                # Check if the candle time is at UTC-5 midnight
                if candle.iso_time.hour == 0 and candle.iso_time.minute == 0:

                    ndog = Level(self.name, level=candle.open)
                    ndog.set_fib_level(0.0, "NDOG", candles=[candle])

                    all_levels.append(ndog)
                    # Add high and low of the New York midnight candle to levels
        except Exception as e:
            logger.critical("NDOG Failed with exception {}".format(e))
        finally:
            return all_levels
