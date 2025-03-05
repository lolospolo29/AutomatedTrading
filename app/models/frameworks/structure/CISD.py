from typing import Optional

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure

class CISD:
    def __init__(self):
        self._consecutive_series_of_candles:int = 0
        self._highest_candle: Optional[Candle] = None  # Can be a Candle or None
        self._lowest_candle: Optional[Candle] = None  # Can be a Candle or None
        self._direction:str = ""

    def add_candle(self, last_candle:Candle) -> Optional[Structure]:
        if self._consecutive_series_of_candles >= 1:
            is_bullish = last_candle.close > last_candle.open
            is_bearish = last_candle.close < last_candle.open

            if self._direction == "Bullish":
                if is_bullish:
                    self._consecutive_series_of_candles += 1
                    self._highest_candle = max(self._highest_candle, last_candle, key=lambda c: c.close)
                    self._lowest_candle = min(self._lowest_candle, last_candle, key=lambda c: c.open)
                elif is_bearish and self._consecutive_series_of_candles >= 3:
                    structure = Structure(name="Consecutive", candles=[self._highest_candle, self._lowest_candle],
                                          direction="Bullish", timeframe=last_candle.timeframe)
                    self._reset_series(last_candle)
                    return structure

            elif self._direction == "Bearish":
                if is_bearish:
                    self._consecutive_series_of_candles += 1
                    self._highest_candle = max(self._highest_candle, last_candle, key=lambda c: c.open)
                    self._lowest_candle = min(self._lowest_candle, last_candle, key=lambda c: c.close)
                elif is_bullish and self._consecutive_series_of_candles >= 3:
                    structure = Structure(name="Consecutive", candles=[self._highest_candle, self._lowest_candle],
                                          direction="Bullish", timeframe=last_candle.timeframe)
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
            return Structure(name="CISD", candles=[first_candle, last_candle], direction="Bearish",timeframe=last_candle.timeframe)

        if is_bullish_cisd:
            return Structure(name="CISD", candles=[first_candle, last_candle], direction="Bullish",timeframe=last_candle.timeframe)

        return None  # No CISD detected

    def _reset_series(self, initialize_candle:Candle):
        self._highest_candle = initialize_candle
        self._lowest_candle = initialize_candle
        self._consecutive_series_of_candles = 1
        self._direction = "Bullish" if initialize_candle.close > initialize_candle.open else "Bearish"