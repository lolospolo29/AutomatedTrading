from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class NWOG:
    """
     ICT new week opening gap is basically the gap between the closing price on friday and the opening price
     on Sunday. This gap may be due to many reasons like geopolitical factors or some fundamental news on
     the weekend which may cause the price to deviate from its closing price
     """

    def __init__(self):
        self.name = 'NWOG'

    def return_levels(self, candles:list[Candle]) -> list[Level]:
        all_levels = []
        try:
            logger.info("Calculating levels for NWOG")
            for candle in candles:
                # Check if the candle time is at UTC-5 midnight
                if candle.iso_time.hour == 0 and candle.iso_time.minute == 0 and candle.iso_time.weekday() == 0:

                    nwog = Level(name=self.name, level=candle.open, direction="", fib_level=candle.close, candles=[candle])
                    nwog.set_fib_level(0.0, "NWOG", candles=[candle])

                    all_levels.append(nwog)
                    # Add high and low of the New York midnight candle to levels
        except Exception as e:
            logger.critical("NWOG Calculation Error with Exception {}".format(e))
        finally:
            return all_levels
