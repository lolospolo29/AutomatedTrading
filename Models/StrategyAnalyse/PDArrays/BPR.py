from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class BPR(IPDArray):
    def __init__(self):
        self.name = "BPR"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        pdArrays = []

        # Lists to store identified FVGs
        bearishFvgList = []
        bullishFvgList = []

        n = len(candles.open)

        # First step: Identify all Fair Value Gaps (FVGs)
        for i in range(2, n):  # Start from the 3rd candle (index 2)
            open1, high1, low1, close1, id1 = candles.open[i - 2], candles.high[i - 2], candles.low[i - 2], \
                                              candles.close[i - 2], candles.id[i - 2]
            open2, high2, low2, close2, id2 = candles.open[i - 1], candles.high[i - 1], \
                                              candles.low[i - 1], \
                                              candles.close[i - 1], candles.id[i - 1]
            open3, high3, low3, close3, id3 = candles.open[i], candles.high[i], candles.low[i], \
                                              candles.close[i], candles.id[i]

            # Check for Bearish FVG (Sell-side FVG)
            if low1 > high3 and close2 < low1:
                bearishFvgList.append({
                    'high': low1,  # Top of FVG range
                    'low': high3,  # Bottom of FVG range
                    'ids': [id1, id2, id3]
                })

            # Check for Bullish FVG (Buy-side FVG)
            if high1 < low3 and close2 > high1:
                bullishFvgList.append({
                    'high': low3,  # Top of FVG range
                    'low': high1,  # Bottom of FVG range
                    'ids': [id1, id2, id3]
                })

        # Second step: Check for overlaps between Bearish and Bullish FVGs
        for sellFvg in bearishFvgList:
            for buyFvg in bullishFvgList:
                # Check for overlap between the two FVGs
                overlapLow = max(sellFvg['low'], buyFvg['low'])
                overlapHigh = min(sellFvg['high'], buyFvg['high'])

                if overlapLow < overlapHigh:
                    # There is an overlap, create a Balanced Price Range (BPR)

                    # Determine the direction based on the order of the FVGs
                    direction = "Bullish"  # Default direction is bullish

                    # If the first FVG (sell_fvg) is Bearish and the second (buy_fvg) is Bullish
                    if sellFvg in bearishFvgList and buyFvg in bullishFvgList:
                        direction = "Bullish"
                    # If the first FVG (buy_fvg) is Bullish and the second (sell_fvg) is Bearish
                    elif buyFvg in bearishFvgList and sellFvg in bullishFvgList:
                        direction = "Bearish"

                    pdArray = PDArray(name=self.name, direction=direction)

                    # Add IDs from both the sell-side and buy-side FVGs
                    for id in sellFvg['ids']:
                        pdArray.addId(id)
                    for id in buyFvg['ids']:
                        pdArray.addId(id)

                    pdArrays.append(pdArray)

        return pdArrays
