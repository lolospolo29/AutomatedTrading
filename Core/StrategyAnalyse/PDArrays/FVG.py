from Core.Main.Asset import Candle
from Core.StrategyAnalyse.PDArray import PDArray
from Interfaces.Strategy.IPDArray import IPDArray


class FVG(IPDArray):
    def __init__(self):
        self.name = "FVG"

    def checkForInverse(self,pdArray: PDArray, candles: list[Candle]) ->str:

        if len(pdArray.Ids) != 3:
            raise ValueError("PDArray must contain exactly 3 IDs.")

        # Extract the two IDs from the PDArray
        id1, id2,id3 = list(pdArray.Ids)

        # Find the indices of these two IDs in the list of candles
        index1 = next((i for i, c in enumerate(candles) if c.id == id1), None)
        index2 = next((i for i, c in enumerate(candles) if c.id == id2), None)
        index3 = next((i for i, c in enumerate(candles) if c.id == id3), None)

        if index1 is None or index2 is None:
            raise ValueError("One or both IDs from PDArray not found in the candle list.")

        # Determine the older index (the one with the higher value)
        older_index = min(index1, index2,index3)

        start_index = older_index + 1

        # Extract and return the candles
        neighbors = candles[start_index:]

        if len(neighbors) > 0:
            for candle in neighbors:
                fvgRange = self.returnCandleRange(pdArray)
                if pdArray.direction == "Bullish":
                    if candle.close < fvgRange.get('low'):
                        return "Bearish"
                if pdArray.direction == "Bearish":
                    if candle.close > fvgRange.get('high'):
                        return "Bullish"
        return pdArray.direction

    def returnCandleRange(self, pdArray: PDArray) -> dict:
        """
        Returns the gap in the FVG.

        :param pdArray: A PDArray object that contains the IDs of the six candles forming the FVG.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]

        low = min(highs)
        high = max(lows)

        # Return the gap range
        return {
            'low': low,
            'high': high
        }

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
        if lookback is not None and len(candles) < lookback:
            return []

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
