import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level


class NDOG:

    def __init__(self):
        self.name = 'NDOG'

    def returnLevels(self, candles: list[Candle]) -> list[Level]:
        allLevels = []

        for candle in candles:
            # Check if the candle time is at UTC-5 midnight
            if candle.isoTime.hour == 0 and candle.isoTime.minute == 0:

                ndog = Level(self.name, level=candle.open)
                ndog.setFibLevel(0.0, "NDOG", candles=[candle])

                allLevels.append(ndog)
                # Add high and low of the New York midnight candle to levels

        return allLevels
