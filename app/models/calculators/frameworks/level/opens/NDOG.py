import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level


class NDOG:

    def __init__(self):
        self.name = 'NDOG'

    def return_levels(self, candles: list[Candle]) -> list[Level]:
        all_levels = []

        for candle in candles:
            # Check if the candle time is at UTC-5 midnight
            if candle.iso_time.hour == 0 and candle.iso_time.minute == 0:

                ndog = Level(self.name, level=candle.open)
                ndog.set_fib_level(0.0, "NDOG", candles=[candle])

                all_levels.append(ndog)
                # Add high and low of the New York midnight candle to levels

        return all_levels
