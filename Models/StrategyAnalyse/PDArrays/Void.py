from Interfaces.Strategy.IPDArray import IPDArray
from Models.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Void(IPDArray):
    def __init__(self):
        self.name = "Void"

    def getCandleRange(self, candles: list[Candle]):
        pass

    def getArrayList(self, candles: list[Candle]) -> list[PDArray]:
        pdArrays = []  # List to store PDArray instances

        for i in range(1, len(candles.close)):
            # Check for a bullish void (upward gap)
            if candles.low[i] > candles.high[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(candles.id[i])
                pdArray.addId(candles.id[i - 1])
                pdArrays.append(pdArray)

            # Check for a bearish void (downward gap)
            elif candles.high[i] < candles.low[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.addId(candles.id[i])
                pdArray.addId(candles.id[i - 1])
                pdArrays.append(pdArray)

        return pdArrays  # Return the list of voids found
