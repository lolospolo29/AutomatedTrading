from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class FVG(IPDArray):
    def __init__(self):
        self.name = "FVG"

    def getCandleRange(self, candles: list[Candle]):
        pass

    def getArrayList(self, candles: list[Candle]) -> list[PDArray]:
        pdArrays = []
        n = len(candles.open)

        # Loop through the data and check 3 consecutive candles for FVGs
        for i in range(2, n):  # Start from the 3rd candle (index 2)
            open1, high1, low1, close1, id1 = candles.open[i - 2], candles.high[i - 2], candles.low[i - 2], \
                                              candles.close[i - 2], candles.id[i - 2]
            open2, high2, low2, close2, id2 = candles.open[i - 1], candles.high[i - 1], \
                                              candles.low[i - 1], \
                                              candles.close[i - 1], candles[i - 1]
            open3, high3, low3, close3, id3 = candles.open[i], candles.high[i], candles.low[i], \
                                              candles.close[i], candles.id[i]

            # Check for Bearish FVG
            if low1 > high3 and close2 < low1:
                pdarray = PDArray(name=self.name, direction='Bearish')
                pdarray.addId(id1)
                pdarray.addId(id2)
                pdarray.addId(id3)
                pdArrays.append(pdarray)

            # Check for Bullish FVG
            elif high1 < low3 and close2 > high1:
                pdarray = PDArray(name=self.name, direction='Bullish')
                pdarray.addId(id1)
                pdarray.addId(id2)
                pdarray.addId(id3)
                pdArrays.append(pdarray)

        return pdArrays
