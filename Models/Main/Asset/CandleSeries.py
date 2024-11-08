from collections import deque

from Models.Main.Asset import Candle


class CandleSeries:
    def __init__(self, timeFrame: int, maxLen: int, broker: str):
        self.candleSeries = deque(maxlen=maxLen)
        self.timeFrame: int = timeFrame
        self.broker: str = broker

    def addCandle(self, candle: Candle) -> None:
        """
        Add new OHLC data to the deque.
        """
        self.candleSeries.append(candle)

    def returnDataByIds(self, searchIds) -> list[Candle]:
        # Collect multiple data points matching the IDs provided
        dataPoints = []

        return dataPoints

    def toList(self) -> list[Candle]:
        """
        Convert the deque of Candle objects into a list.
        """
        return list(self.candleSeries)