from typing import Optional

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure


class BOS:

    def __init__(self):
        self._bullish_a: Optional[Candle, None] = None
        self._bullish_b: Optional[Candle, None] = None
        self._bullish_is_valid = False

        self._bearish_a: Optional[Candle, None] = None
        self._bearish_b: Optional[Candle, None] = None
        self._bearish_is_valid = False

    def detect_bos(self, last_candle: Candle) -> Optional[Structure]:

        struct = None

        if last_candle.close > last_candle.open:
            if self._bullish_a is None:
                self._bullish_a = last_candle
            if self._bullish_a.high < last_candle.close and self._bullish_is_valid:
                if self._bullish_a.iso_time < self._bullish_b.iso_time:
                    struct = Structure(name="BOS", direction="Bullish", candles=[self._bullish_a, self._bullish_b]
                                       , timeframe=last_candle.timeframe)
                    self._structure_reset_bullish(last_candle)

            if last_candle.close > last_candle.high:
                self._bullish_a = last_candle

        if last_candle.close < last_candle.open:
            if self._bearish_a is None:
                self._bearish_a: Candle = last_candle
            if self._bearish_a.low > last_candle.close and self._bearish_is_valid:
                if self._bearish_a.iso_time < self._bearish_b.iso_time:
                    struct = Structure(name="BOS", direction="Bearish", candles=[self._bearish_a, self._bearish_b]
                                       , timeframe=last_candle.timeframe)
                    self._structure_reset_bearish(last_candle)

            if last_candle.close < self._bearish_a.low:
                self._bearish_a = last_candle

        self._set_b_if_empty(last_candle)

        self._check_b_leg_condition(last_candle)

        if struct:
            return struct

    def _set_b_if_empty(self, last_candle: Candle):
        if self._bullish_b is None:
            self._bullish_b = last_candle
        if self._bearish_b is None:
            self._bearish_b = last_candle

    def _check_b_leg_condition(self, last_candle: Candle):
        if last_candle.close < self._bullish_b.low and self._bullish_a:
            self._bullish_b = last_candle
            self._bullish_is_valid = True
        if last_candle.close > self._bearish_b.high and self._bearish_a:
            self._bearish_b = last_candle
            self._bearish_is_valid = True

    def _structure_reset_bullish(self, last_candle: Candle):
        self._bullish_a = last_candle
        self._bullish_b = None
        self._bullish_is_valid = False
        self._bearish_a = None
        self._bearish_b = None
        self._bearish_is_valid = False

    def _structure_reset_bearish(self, last_candle: Candle):
        self._bullish_a = None
        self._bullish_b = None
        self._bullish_is_valid = False
        self._bearish_a = last_candle
        self._bearish_b = None
        self._bearish_is_valid = False