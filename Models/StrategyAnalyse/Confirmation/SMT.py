from typing import Any

from Interfaces.Strategy.IConfirmation import IConfirmation
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Structure import Structure


class SMT(IConfirmation):
    def returnConfirmation(self, candlesAsset1: list[Candle], candlesAsset2: list[Candle]) -> Any:
        """
        Determine if an SMT divergence is detected between two asset data points.

        Parameters:
        data_points_asset1 (list): Data points for asset 1.
        data_points_asset2 (list): Data points for asset 2.

        Returns:
        bool: True if SMT divergence detected, False otherwise.
        """

        # Check for swing highs and lows
        for i in range(1, len(candlesAsset1) - 1):
            high1 = candlesAsset1[i][1]  # High of asset 1
            high2 = candlesAsset2[i][1]  # High of asset 2
            low1 = candlesAsset1[i][2]   # Low of asset 1
            low2 = candlesAsset2[i][2]   # Low of asset 2

            # Check for divergence in swing highs
            if high1 > high1[i-1] and high1 > high1[i+1] and high2 < high2[i-1] and high2 < high2[i+1]:
                return Structure(name="SMT", direction="Bearish")  # Bearish divergence detected

            # Check for divergence in swing lows
            if low1 < low1[i-1] and low1 < low1[i+1] and low2 > low2[i-1] and low2 > low2[i+1]:
                return Structure(name="SMT", direction="Bullish")  # Bullish divergence detected
