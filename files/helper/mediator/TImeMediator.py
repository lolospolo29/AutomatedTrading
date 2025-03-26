import threading
from typing import Optional

from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level
from files.models.frameworks.time.Asia import Asia
from files.models.frameworks.time.CBDR import CBDRPM
from files.models.frameworks.time.London import LondonOpen
from files.models.frameworks.time.NYOpen import NYOpen

class TimeMediator:
    def __init__(self):
        self._lock = threading.Lock()

        self._asia_session = Asia()
        self._london_session = LondonOpen()
        self._ny_session = NYOpen()
        self._cbdr = CBDRPM()

        self._session_level:list[Level] = []

        self._current_session:Optional[str] = None

        self._current_session_high_candle: Optional[Candle] = None
        self._current_session_low_candle: Optional[Candle] = None

    def analyze(self,last_candle:Candle):
        with self._lock:
            if last_candle.timeframe <= 30:
                if self._asia_session.is_in_entry_window(last_candle.iso_time):
                    self._set_current_session_hl(last_candle)
                    self._current_session = self._asia_session.name
                    return
                if self._london_session.is_in_entry_window(last_candle.iso_time):
                    self._set_current_session_hl(last_candle)
                    self._current_session = self._london_session.name
                    return
                if self._ny_session.is_in_entry_window(last_candle.iso_time):
                    self._set_current_session_hl(last_candle)
                    self._current_session = self._ny_session.name
                    return
                if self._cbdr.is_in_entry_window(last_candle.iso_time):
                    self._set_current_session_hl(last_candle)
                    self._current_session = self._ny_session.name
                    return
                self._create_new_level()

    def get_session_level(self):
        with self._lock:
            return self._session_level

    def remove_old_sessions(self,_ids):
        with self._lock:
            self._current_session = [imbalances for imbalances in self._current_session
                                     if all(candle.strategy_id in _ids for candle in imbalances.candles)]

    def clear(self):
        with self._lock:
            self._session_level = []
            self._current_session = None
            self._current_session_high_candle = None
            self._current_session_low_candle = None

    def _create_new_level(self):
        if self._current_session_high_candle is not None and self._current_session_low_candle is not None:
            self._session_level.append(Level(candles=[self._current_session_high_candle, self._current_session_low_candle]
                                             ,level=0,fib_level=0,name=self._current_session))
            self._current_session = None
            self._current_session_high_candle = None
            self._current_session_low_candle = None

    def _set_current_session_hl(self,candle:Candle):
        if self._current_session_high_candle is None:
            self._current_session_high_candle = candle
        if self._current_session_low_candle is None:
            self._current_session_low_candle = candle
        if self._current_session_high_candle.high < candle.high:
            self._current_session_high_candle = candle
        if self._current_session_low_candle.low < candle.low:
            self._current_session_low_candle = candle