from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle


class Swings(IPDArray):  # id need to be fixed
    def __init__(self):
        self.name = "Swing"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        swingList = []  # List to store PDArray objects

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        pass
