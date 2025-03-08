import bisect
from collections import deque
from pydantic import BaseModel

from files.models.asset.Candle import Candle


class CandleSeries(BaseModel):
    candleSeries: deque
    timeFrame: int
    broker: str

    def add_candle(self, candle: Candle) -> None:
        candleList = list(self.candleSeries)

        # Find the correct position to insert using bisect (binary search)
        index = bisect.bisect_right([c.iso_time for c in candleList], candle.iso_time)

        # Insert the new candle at the correct position
        candleList.insert(index, candle)

        # After insertion, we recreate the deque from the sorted list
        self.candleSeries = deque(candleList, maxlen=self.candleSeries.maxlen)

        # Ensure deque size does not exceed maxLen
        if len(self.candleSeries) > self.candleSeries.maxlen:
            self.candleSeries.pop()

    def return_candle_i_ds(self) -> list:
        """
        Returns a list of all candle IDs in the series.
        """
        return [candle.id for candle in self.candleSeries]

    def to_list(self) -> list[Candle]:
        """
        Convert the deque of Candle objects into a list.
        """
        return list(self.candleSeries)
