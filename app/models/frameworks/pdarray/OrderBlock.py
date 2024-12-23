from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class Orderblock(IPDArray):
    def __init__(self):
        self.name: str = "OB"

    def checkForInverse(self, pdArray: PDArray, candles: list[Candle]) -> str:

        if len(pdArray.Ids) != 2:
            raise ValueError("PDArray must contain exactly 3 IDs.")

        # Extract the two IDs from the PDArray
        id1, id2 = list(pdArray.Ids)

        # Find the indices of these two IDs in the list of candles
        index1 = next((i for i, c in enumerate(candles) if c.id == id1), None)
        index2 = next((i for i, c in enumerate(candles) if c.id == id2), None)

        if index1 is None or index2 is None:
            raise ValueError("One or both IDs from PDArray not found in the candle list.")

        # Determine the older index (the one with the higher value)
        older_index = min(index1, index2)

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
        Returns the high and low of the OB.

        :param pdArray: A PDArray object that contains candles.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """

        # Extract prices from the candles
        highs = [candle.high for candle in pdArray.candles]
        lows = [candle.low for candle in pdArray.candles]

        high = max(highs)
        low = min(lows)

        return {
            'low': low,
            'high': high
        }

    def returnArrayList(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        # Step 1: Apply lookback to limit the range of candles
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

        if lookback is not None and len(candles) < lookback:
            return []

        if len(candles) < 2:
            return []

        pdArrays = []

        # Extract data points
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        n = len(highs)

        # Loop through the data and check 3 consecutive candles for FVGs
        for i in range(1, n):  # Start bei der 2. Kerze (Index 1)
            open1, high1, low1, close1, id1 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1], ids[i - 1]
            open2, high2, low2, close2, id2 = opens[i], highs[i], lows[i], close[i], ids[i]

            if close1 < open1 and close2 > open2 and low1 > low2:
                pdArray = PDArray(name="OB",direction="Bullish")
                pdArray.addId(id1)
                pdArray.addId(id2)
                pdArrays.append(pdArray)
            if close1 > open1 and close2 < open2 and high1 < high2:
                pdArray = PDArray(name="OB",direction="Bearish")
                pdArray.addId(id1)
                pdArray.addId(id2)
                pdArrays.append(pdArray)
        return pdArrays