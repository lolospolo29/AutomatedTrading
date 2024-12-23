from typing import Any

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure


class SMT:
    def __init__(self):
        self.name = "SMT"

    def returnConfirmation(self, candlesAsset1: list[Candle], candlesAsset2: list[Candle]) -> list[Structure]:
        """
        Determine if an SMT divergence is detected between two asset data points.

        Parameters:
        data_points_asset1 (list): Data points for asset 1.
        data_points_asset2 (list): Data points for asset 2.

        """

        last_candle_asset1 = candlesAsset1[-1]
        last_candle_asset2 = candlesAsset2[-1]

        # Compare isoTime values
        if last_candle_asset1.isoTime != last_candle_asset2.isoTime:
            return False

        if len(candlesAsset1) != len(candlesAsset2):
            return False
        highs1 = []
        ids1 = []
        highs2 = []
        lows1 = []
        ids2 = []
        lows2 = []

        for candle in candlesAsset1:
            highs1.append(candle.high)
            lows1.append(candle.low)
        for candle in candlesAsset2:
            highs2.append(candle.high)
            lows2.append(candle.low)
        # Check for swing highs and lows
        for i in range(1, len(highs1) - 1):
            high1 = highs1[i]  # High of asset 1
            high2 = highs2[i]  # High of asset 2
            low1 = lows1[i]   # Low of asset 1
            low2 = lows2[i]   # Low of asset 2

            # Check for divergence in swing highs
            if high1 > high1[i-1] and high1 > high1[i+1] and high2 < high2[i-1] and high2 < high2[i+1]:
                return Structure(self.name, direction="Bearish", id= ids1[i+1])  # Bearish divergence detected

            # Check for divergence in swing lows
            if low1 < low1[i-1] and low1 < low1[i+1] and low2 > low2[i-1] and low2 > low2[i+1]:
                return Structure(self.name, direction="Bullish", id=ids2[i+1])  # Bullish divergence detected
