import threading
from typing import List

from app.models.asset.Candle import Candle


class SMTHandler:
    """
    Handles and manages candles for a pair of assets from different brokers,
    providing thread-safe operations for storing, retrieving, and synchronizing
    candles. The class maintains separate candle storage for each asset,
    categorized by timeframes, and ensures proper synchronization across
    assets.
    """
    def __init__(self, asset_1: str, asset_2: str,correlation:str):

        self.asset_1 = asset_1
        self.asset_2 = asset_2
        self.correlation = correlation
        self.candles_asset_1 = {}
        self.candles_asset_2 = {}

        self._lock = threading.Lock()

    def add_candle(self, candle: Candle) -> None:
        """
        Adds a Candle to the appropriate asset's candle list, ensuring thread safety.

        Parameters:
            candle (Candle): The Candle to add.

        Raises:
            ValueError: If the candle's asset is neither of the two managed assets.
        """
        with self._lock:
            if candle.asset == self.asset_1:
                self._add_to_candle_list(self.candles_asset_1, candle)
            elif candle.asset == self.asset_2:
                self._add_to_candle_list(self.candles_asset_2, candle)
            else:
                raise ValueError(
                    f"Candle asset '{candle.asset}' is not part of the pair '{self.asset_1}/{self.asset_2}'.")

    def get_synchronized_candles(self, timeframe: int) -> tuple[list[Candle], list[Candle]]:
        """
        Returns synchronized lists of candles for both assets at the specified timeframe.

        Parameters:
            timeframe (int): The timeframe (e.g., 1, 5, 15 minutes).

        Returns:
            (List[Candle], List[Candle]): Two lists of synchronized Candle objects.

        Raises:
            ValueError: If no candles are available for the specified timeframe.
        """
        with self._lock:
            if timeframe not in self.candles_asset_1 or timeframe not in self.candles_asset_2:
                raise ValueError(f"No candles available for timeframe '{timeframe}'.")

            # Retrieve candles for both assets
            candles_1 = self.candles_asset_1[timeframe]
            candles_2 = self.candles_asset_2[timeframe]

            # Synchronize the candle lists based on iso_time
            synchronized_1, synchronized_2 = self._synchronize_candles_by_time(candles_1, candles_2)

            return synchronized_1, synchronized_2

    @staticmethod
    def _add_to_candle_list(candle_dict: dict, candle: Candle) -> None:
        """
        Adds a Candle to a specific dictionary by timeframe.

        Parameters:
            candle_dict (dict): The dictionary to which the candle should be added.
            candle (Candle): The Candle to add.
        """
        if candle.timeframe not in candle_dict:
            candle_dict[candle.timeframe] = []
        candle_dict[candle.timeframe].append(candle)

    @staticmethod
    def _synchronize_candles_by_time(
            candles_1: List[Candle], candles_2: List[Candle]
    ) -> tuple[list[Candle], list[Candle]]:
        """
        Synchronizes two lists of candles so they have the same length and match on `iso_time`.

        Parameters:
            candles_1 (List[Candle]): Candles for the first asset.
            candles_2 (List[Candle]): Candles for the second asset.

        Returns:
            (List[Candle], List[Candle]): Two lists of synchronized Candle objects.
        """
        # Create dictionaries with iso_time as the key for fast lookup
        candles_dict_1 = {c.iso_time: c for c in candles_1}
        candles_dict_2 = {c.iso_time: c for c in candles_2}

        # Find common iso_times
        common_times = sorted(set(candles_dict_1.keys()).intersection(candles_dict_2.keys()))

        # Build synchronized lists
        synchronized_1 = [candles_dict_1[time] for time in common_times]
        synchronized_2 = [candles_dict_2[time] for time in common_times]

        return synchronized_1, synchronized_2
