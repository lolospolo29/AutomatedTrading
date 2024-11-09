import bisect
from collections import deque

from Models.Main.Asset import Candle


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

    def returnDataByIds(self, searchIds) -> list[Candle]:
        # Collect multiple data points matching the IDs provided
        dataPoints = []

        return dataPoints

    def toList(self) -> list[Candle]:
        """
        Convert the deque of Candle objects into a list.
        """
        return list(self.candleSeries)