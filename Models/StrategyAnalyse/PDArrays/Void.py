from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Void(IPDArray):
    def __init__(self):
        self.name = "Void"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list:

        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
        if lookback is not None and len(candles) < lookback:
            return []
        pdArrays = []  # List to store PDArray instances

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        for i in range(1, len(close)):
            # Check for a bullish void (upward gap)
            if lows[i] > highs[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bullish")
                pdArray.addId(ids[i])
                pdArray.addId(ids[i - 1])
                pdArrays.append(pdArray)

            # Check for a bearish void (downward gap)
            elif highs[i] < lows[i - 1]:
                pdArray = PDArray(name=self.name, direction="Bearish")
                pdArray.addId(ids[i])
                pdArray.addId(ids[i - 1])
                pdArrays.append(pdArray)

        return pdArrays  # Return the list of voids found
