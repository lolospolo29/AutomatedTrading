from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class BPR(IPDArray):
    def __init__(self):
        self.name = "BPR"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        if len(candles) < 6 :
            return []

        pdArrays = []

        # Lists to store identified FVGs
        bearishFvgList = []
        bullishFvgList = []

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        n = len(opens)

        # First step: Identify all Fair Value Gaps (FVGs)
        for i in range(2, n):  # Start from the 3rd candle (index 2)
            open1, high1, low1, close1, id1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2], ids[i - 2]
            open2, high2, low2, close2, id2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1], ids[i - 1]
            open3, high3, low3, close3, id3 = opens[i], highs[i], lows[i], close[i], ids[i]

            # Check for Bearish FVG (Sell-side FVG)
            if low1 > high3 and close2 < low1:
                bearishFvgList.append({
                    'high': low2,  # Top of FVG range
                    'low': high2,  # Bottom of FVG range
                    'ids': [id1, id2, id3],
                    'index': [i, i-1,i-2]
                })

            # Check for Bullish FVG (Buy-side FVG)
            if high1 < low3 and close2 > high1:
                bullishFvgList.append({
                    'high': low2,  # Top of FVG range
                    'low': high2,  # Bottom of FVG range
                    'ids': [id1, id2, id3],
                    'index': [i, i - 1, i - 2]
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
                    if max(sellFvg['index']) < max(buyFvg['index']):
                        direction = "Bullish"
                    # If the first FVG (buy_fvg) is Bullish and the second (sell_fvg) is Bearish
                    if max(sellFvg['index']) > max(buyFvg['index']):
                        direction = "Bearish"

                    pdArray = PDArray(name=self.name, direction=direction)

                    # Add IDs from both the sell-side and buy-side FVGs
                    for id in sellFvg['ids']:
                        pdArray.addId(id)
                    for id in buyFvg['ids']:
                        pdArray.addId(id)

                    pdArrays.append(pdArray)

        return pdArrays
