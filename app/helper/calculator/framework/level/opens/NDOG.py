from app.helper.calculator.framework.level.LevelEnum import LevelEnum
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class NDOG:
    """ The NDOG is the gap between the opening price and closing price of the previous day"""
    def __init__(self):
        self.name = LevelEnum.NEWYORKDAILYOPENGAP.value

    def return_levels(self, candles: list[Candle]) -> list[Level]:
        all_levels = []
        try:
            last_candle:Candle = candles[-1]
            logger.info("Calculating NDOG levels...")
            for candle in candles:
                # Check if the candle time is at UTC-5 midnight
                if candle.iso_time.hour == 0 and candle.iso_time.minute == 0:

                    ndog = Level(name=self.name, level=candle.close - candle.open,direction="",fib_level=candle.open
                                 ,candles =[candle],timeframe=last_candle.timeframe)
                    ndog.set_fib_level(0.0, "NDOG", candles=[candle])

                    all_levels.append(ndog)
                    # Add high and low of the New York midnight candle to levels
        except Exception as e:
            logger.critical("NDOG Failed with exception {}".format(e))
        finally:
            return all_levels
