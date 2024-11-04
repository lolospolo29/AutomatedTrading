from Interfaces.Strategy.IPDArray import IPDArray
from Models.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class LiquidityVoid(IPDArray):
    def __init__(self, minCandlesInRow: int):
        self.minCandlesInRow: int = minCandlesInRow
        self.name: str = "LV"

    def getCandleRange(self, candles: list[Candle]):
        pass

    def getArrayList(self, candles: list[Candle]) -> list[PDArray]:
        MinCandlesInRow = self.minCandlesInRow
        pdArrays = []
        rowCandles = 0
        direction = None

        # Loop through all candles in the data
        for i in range(1, len(candles.close)):
            # Check if the current candle is bullish or bearish
            currentDirection = 'Bullish' if candles.close[i] > candles.open[i] else 'Bearish'

            # If it's the first candle, set the direction
            if direction is None:
                direction = currentDirection
                rowCandles = 1
            # If the current candle is in the same direction as the previous one
            elif currentDirection == direction:
                rowCandles += 1
            # If the direction changes
            else:
                # If there are enough candles in the row, create a new PDArray
                if rowCandles >= MinCandlesInRow:
                    pdArray = PDArray(self.name, direction)

                    # Add the candle data to the PDArray
                    for j in range(i - rowCandles, i):
                        pdArray.addId(candles.id[j])

                    pdArrays.append(pdArray)

                # Reset for the new direction
                direction = currentDirection
                rowCandles = 1

        # Handle the case where the last set of candles forms a valid sequence
        if rowCandles >= MinCandlesInRow:
            pdArray = PDArray(self.name, direction)

            for j in range(len(candles.close) - rowCandles, len(candles.close)):
                pdArray.addId(candles.id[j])

            pdArrays.append(pdArray)

        return pdArrays
