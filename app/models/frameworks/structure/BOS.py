from typing import Optional

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure


class BOS:

    def __init__(self):
        self.bullish_a: Optional[Candle, None] = None
        self.bullish_b: Optional[Candle, None] = None
        self.bullish_is_valid = False

        self.bearish_a: Optional[Candle, None] = None
        self.bearish_b: Optional[Candle, None] = None
        self.bearish_is_valid = False

    def return_confirmation(self, last_candle: Candle) -> Optional[Structure]:

        struct = None

        if last_candle.close > last_candle.open:
            if self.bullish_a is None:
                self.bullish_a = last_candle
            if self.bullish_a.high < last_candle.close and self.bullish_is_valid:
                if self.bullish_a.iso_time < self.bullish_b.iso_time:
                    struct = Structure(name="BOS", direction="Bullish", candles=[self.bullish_a, self.bullish_b]
                                       , timeframe=last_candle.timeframe)
                    self._structure_reset_bullish(last_candle)

            if last_candle.close > last_candle.high:
                self.bullish_a = last_candle

        if last_candle.close < last_candle.open:
            if self.bearish_a is None:
                self.bearish_a: Candle = last_candle
            if self.bearish_a.low > last_candle.close and self.bearish_is_valid:
                if self.bearish_a.iso_time < self.bearish_b.iso_time:
                    struct = Structure(name="BOS", direction="Bearish", candles=[self.bearish_a, self.bearish_b]
                                       , timeframe=last_candle.timeframe)
                    self._structure_reset_bearish(last_candle)

            if last_candle.close < self.bearish_a.low:
                self.bearish_a = last_candle

        self._set_b_if_empty(last_candle)

        self._check_b_leg_condition(last_candle)

        if struct:
            return struct

    def _set_b_if_empty(self, last_candle: Candle):
        if self.bullish_b is None:
            self.bullish_b = last_candle
        if self.bearish_b is None:
            self.bearish_b = last_candle

    def _check_b_leg_condition(self, last_candle: Candle):
        if last_candle.close < self.bullish_b.low and self.bullish_a:
            self.bullish_b = last_candle
            self.bullish_is_valid = True
        if last_candle.close > self.bearish_b.high and self.bearish_a:
            self.bearish_b = last_candle
            self.bearish_is_valid = True

    def _structure_reset_bullish(self, last_candle: Candle):
        self.bullish_a = last_candle
        self.bullish_b = None
        self.bullish_is_valid = False
        self.bearish_a = None
        self.bearish_b = None
        self.bearish_is_valid = False

    def _structure_reset_bearish(self, last_candle: Candle):
        self.bullish_a = None
        self.bullish_b = None
        self.bullish_is_valid = False
        self.bearish_a = last_candle
        self.bearish_b = None
        self.bearish_is_valid = False