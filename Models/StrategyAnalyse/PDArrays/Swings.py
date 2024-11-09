from Interfaces.Strategy.IPDArray import IPDArray
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.PDArray import PDArray


class Swings(IPDArray):  # id need to be fixed
    def __init__(self):
        self.name = "Swing"

    def returnCandleRange(self, candles: list[Candle]):
        pass

    def returnArrayList(self, candles: list[Candle]) -> list:
        swingList = []  # List to store PDArray objects

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        # Variables for storing points used in calculation
        a = b = c = d = e = None
        aId = bId = cId = dId = eId = None  # Add variables to track the IDs of data points

        # Iterate over the data points, similar to Pine Script logic
        for i in range(1, len(close) - 1):
            ph = self.isPivotHigh(highs, i)  # Pivot High
            pl = self.isPivotLow(lows, i)  # Pivot Low

            if not (ph or pl):  # No swing point
                continue

            # Update points and their IDs
            a = close[i]
            aId = ids[i]  # Assuming 'ids' is a list of unique IDs for each data point

            if b is None:
                b = a
                bId = aId
            elif c is None:
                c = b
                cId = bId
                b = a
                bId = aId
            elif d is None:
                d = c
                dId = cId
                c = b
                cId = bId
                b = a
                bId = aId
            else:
                e = d
                eId = dId
                d = c
                dId = cId
                c = b
                cId = bId
                b = a
                bId = aId

            # Detect Higher High (HH)
            if a > b and a > c and c > b and c > d:
                hhPdarray = PDArray("HH", "Bullish")
                hhPdarray.addId(aId)
                hhPdarray.addId(bId)
                hhPdarray.addId(cId)
                hhPdarray.addId(dId)
                swingList.append(hhPdarray)  # Add to the list

            # Detect Lower Low (LL)
            if a < b and a < c and c < b and c < d:
                llPdarray = PDArray("LL", "Bearish")
                llPdarray.addId(aId)
                llPdarray.addId(bId)
                llPdarray.addId(cId)
                llPdarray.addId(dId)
                swingList.append(llPdarray)  # Add to the list

            # Detect Higher Low (HL)
            if (a >= c and b > c and d > c and d > e) or (a < b and a > c and b < d):
                hlPdarray = PDArray("HL", "Bullish")
                hlPdarray.addId(aId)
                hlPdarray.addId(bId)
                hlPdarray.addId(cId)
                hlPdarray.addId(dId)
                if eId is not None:
                    hlPdarray.addId(eId)
                swingList.append(hlPdarray)  # Add to the list

            # Detect Lower High (LH)
            if (a <= c and b < c and d < c and d < e) or (a > b and a < c and b > d):
                lh_pdarray = PDArray("LH", "Bearish")
                lh_pdarray.addId(aId)
                lh_pdarray.addId(bId)
                lh_pdarray.addId(cId)
                lh_pdarray.addId(dId)
                if eId is not None:
                    lh_pdarray.addId(eId)
                swingList.append(lh_pdarray)  # Add to the list

        # Return the list of PDArray objects (one for each swing point)
        return swingList

    # Helper function to check for pivot highs and lows
    @staticmethod
    def isPivotHigh(highs: list, index: int):
        lb = 5  # Left Bars
        rb = 5  # Right Bars
        if index >= lb and index < len(highs) - rb:
            leftMax = max(highs[index - lb:index])
            rightMax = max(highs[index + 1:index + rb + 1])
            return highs[index] > leftMax and highs[index] > rightMax
        return False

    @staticmethod
    def isPivotLow(lows: list, index: int):
        lb = 5  # Left Bars
        rb = 5  # Right Bars
        if index >= lb and index < len(lows) - rb:
            leftMin = min(lows[index - lb:index])
            rightMin = min(lows[index + 1:index + rb + 1])
            return lows[index] < leftMin and lows[index] < rightMin
        return False
