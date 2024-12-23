import bisect
from collections import deque

from app.models.asset import Candle


class CandleSeries:

    def __init__(self, timeFrame: int, maxLen: int, broker: str):
        self.candleSeries = deque(maxlen=maxLen)
        self.timeFrame: int = timeFrame
        self.broker: str = broker

    def addCandle(self, candle: Candle) -> None:
        candleList = list(self.candleSeries)

        # Find the correct position to insert using bisect (binary search)
        index = bisect.bisect_right([c.isoTime for c in candleList], candle.isoTime)

        # Insert the new candle at the correct position
        candleList.insert(index, candle)

        # After insertion, we recreate the deque from the sorted list
        self.candleSeries = deque(candleList, maxlen=self.candleSeries.maxlen)

        # Ensure deque size does not exceed maxLen
        if len(self.candleSeries) > self.candleSeries.maxlen:
            self.candleSeries.pop()

    def returnCandleIDs(self) -> list:
        """
        Returns a list of all candle IDs in the series.
        """
        return [candle.id for candle in self.candleSeries]

    def toList(self) -> list[Candle]:
        """
        Convert the deque of Candle objects into a list.
        """
        return list(self.candleSeries)