from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class FVG(IPDArray):
    def __init__(self):
        self.name = "FVG"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        pdArrays = []
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        n = len(opens)
        if n > 2:
            # Loop through the data and check 3 consecutive candles for FVGs
            for i in range(2, n):  # Start bei der 3. Kerze (Index 2)
                open1, high1, low1, close1, id1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2], ids[i - 2]
                open2, high2, low2, close2, id2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1], ids[i - 1]
                open3, high3, low3, close3, id3 = opens[i], highs[i], lows[i], close[i], ids[i]

                # Überprüfung auf Bearish FVG
                if low1 > high3 and close2 < low1:
                    pdarray = PDArray(name=self.name, direction='Bearish')
                    pdarray.addId(id1)
                    pdarray.addId(id2)
                    pdarray.addId(id3)
                    pdArrays.append(pdarray)

                # Überprüfung auf Bullish FVG
                elif high1 < low3 and close2 > high1:
                    pdarray = PDArray(name=self.name, direction='Bullish')
                    pdarray.addId(id1)
                    pdarray.addId(id2)
                    pdarray.addId(id3)
                    pdArrays.append(pdarray)

            return pdArrays
