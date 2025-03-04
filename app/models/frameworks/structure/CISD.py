from typing import Optional

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure

class CISD:
    def __init__(self):
        self.consecutive_series_of_candles:int = 0
        self.highest_candle: Optional[Candle] = None  # Can be a Candle or None
        self.lowest_candle: Optional[Candle] = None  # Can be a Candle or None
        self.direction:str = ""

    def add_candle(self, last_candle:Candle) -> Optional[Structure]:
        if self.consecutive_series_of_candles >= 1:
            is_bullish = last_candle.close > last_candle.open
            is_bearish = last_candle.close < last_candle.open

            if self.direction == "Bullish":
                if is_bullish:
                    self.consecutive_series_of_candles += 1
                    self.highest_candle = max(self.highest_candle, last_candle, key=lambda c: c.close)
                    self.lowest_candle = min(self.lowest_candle, last_candle, key=lambda c: c.open)
                elif is_bearish and self.consecutive_series_of_candles >= 3:
                    structure = Structure(name="Consecutive", candles=[self.highest_candle, self.lowest_candle],
                                          direction="Bullish")
                    self._reset_series(last_candle)
                    return structure

            elif self.direction == "Bearish":
                if is_bearish:
                    self.consecutive_series_of_candles += 1
                    self.highest_candle = max(self.highest_candle, last_candle, key=lambda c: c.open)
                    self.lowest_candle = min(self.lowest_candle, last_candle, key=lambda c: c.close)
                elif is_bullish and self.consecutive_series_of_candles >= 3:
                    structure = Structure(name="Consecutive", candles=[self.highest_candle, self.lowest_candle],
                                          direction="Bullish")
                    self._reset_series(last_candle)
                    return structure
        else:
            self._reset_series(last_candle)

    @staticmethod
    def check_for_cisd(last_candle: Candle, consecutive: Structure) -> Optional[Structure]:

        first_candle = consecutive.candles[0]  # The first candle in the consecutive structure
        is_bearish_cisd = last_candle.close < first_candle.open and consecutive.direction == "Bullish"
        is_bullish_cisd = last_candle.close > first_candle.open and consecutive.direction == "Bearish"

        if is_bearish_cisd:
            return Structure(name="CISD", candles=[first_candle, last_candle], direction="Bearish")

        if is_bullish_cisd:
            return Structure(name="CISD", candles=[first_candle, last_candle], direction="Bullish")

        return None  # No CISD detected

    def _reset_series(self, initialize_candle:Candle):
        self.highest_candle = initialize_candle
        self.lowest_candle = initialize_candle
        self.consecutive_series_of_candles = 1
        self.direction = "Bullish" if initialize_candle.close > initialize_candle.open else "Bearish"