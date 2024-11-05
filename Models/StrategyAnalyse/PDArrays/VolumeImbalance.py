from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class VolumeImbalance(IPDArray):
    def __init__(self):
        self.name = "VI"

    def getCandleRange(self, candles: list[Candle]):
        pass

    def getArrayList(self, candles: list[Candle]) -> list[PDArray]:
        pdArrays = []  # List to store PDArray instances

        for i in range(1, len(candles.close)):
            # Check for a bullish vi
            if min(candles.open[i], candles.close[i]) > candles.high[i - 1] and \
                    candles.low[i] > max(candles.open[i - 1], candles.close[-1]) and \
                    (candles.low[i] < candles.high[i - 1]):
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(candles.id[i])
                pdArray.addId(candles.id[i - 1])
                pdArrays.append(pdArray)

            # Check for a bearish vi
            elif max(candles.open[i], candles.close[i]) < candles.low[i - 1] and \
                    candles.high[i] < min(candles.open[i - 1], candles.close[-1]) and \
                    (candles.high[i] > candles.low[i - 1]):
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.addId(candles.id[i])
                pdArray.addId(candles.id[i - 1])
                pdArrays.append(pdArray)

        return pdArrays  # Return the list of voids found
