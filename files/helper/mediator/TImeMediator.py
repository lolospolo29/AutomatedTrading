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

        self._current_session_high: Optional[Candle] = None
        self._current_session_low: Optional[Candle] = None

    def analyze(self,last_candle:Candle):
        with self._lock:
            pass