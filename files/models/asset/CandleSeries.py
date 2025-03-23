import bisect
from collections import deque

from pydantic import BaseModel

from files.models.asset.Candle import Candle

class CandleSeries(BaseModel):
    candle_series: deque
    time_frame: int
    broker: str

    def add_candle(self, candle: Candle) -> None:
        candleList = list(self.candle_series)

        index = bisect.bisect_right([c.iso_time for c in candleList], candle.iso_time)

        candleList.insert(index, candle)

        self.candle_series = deque(candleList, maxlen=self.candle_series.maxlen)

        if len(self.candle_series) > self.candle_series.maxlen:
            self.candle_series.pop()