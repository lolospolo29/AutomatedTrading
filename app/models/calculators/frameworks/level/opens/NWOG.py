import sys

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level


class NWOG:

    def __init__(self):
        self.name = 'NWOG'

    def returnLevels(self, candles:list[Candle]) -> list[Level]:
        allLevels = []

        for candle in candles:
            # Check if the candle time is at UTC-5 midnight
            if candle.isoTime.hour == 0 and candle.isoTime.minute == 0 and candle.isoTime.weekday() == 0:

                nwog = Level(self.name, level=candle.open)
                nwog.setFibLevel(0.0, "NWOG", candles=[candle])

                allLevels.append(nwog)
                # Add high and low of the New York midnight candle to levels

        return allLevels
