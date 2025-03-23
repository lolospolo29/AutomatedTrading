import threading
from typing import Optional

from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from files.models.frameworks.level.equalHL import equalHL
from files.models.frameworks.pdarray.Swing import Swing
from files.models.frameworks.structure.BOS import BOS
from files.models.frameworks.structure.CISD import CISD
from files.models.frameworks.structure.Choch import Choch
from files.models.frameworks.structure.MSS import MSS
from files.models.frameworks.structure.MitigationBlock import MitigationBlock


class StructureMediator:
    def __init__(self):
        self._lock = threading.Lock()

        self._swings: dict[int, list[PDArray]] = {}
        self._consecutive_candles: dict[int, list[Structure]] = {}
        self._current_mss: dict[int, Structure] = {}
        self._previous_mss: dict[int, Structure] = {}
        self._current_bos: dict[int, Structure] = {}
        self._previous_bos: dict[int, Structure] = {}
        self._current_cisd: dict[int, Structure] = {}
        self._eqhl: dict[int, list[Level]] = {}
        self._bos: dict[int, BOS] = {}
        self._cisd: dict[int, CISD] = {}

    def analyze(self,first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe,atr:float):
        with self._lock:
            self._detect_swing(first_candle, second_candle, third_candle, timeframe)
            self._detect_eqhl(timeframe,atr)

            self._detect_mss(third_candle, timeframe)
            self._detect_bos(third_candle, timeframe)
            self._detect_consecutive(third_candle, timeframe)
            self._detect_cisd(third_candle, timeframe)

            self._detect_choch(timeframe)

            self._detect_liquidity_sweep(third_candle, timeframe)
            self._detect_mitigation_block(timeframe)

            self._remove_duplicate_consecutive_candles(timeframe)
            self._remove_duplicate_eqhl(timeframe)
            self._remove_duplicate_consecutive_candles(timeframe)
            self._remove_duplicate_swings(timeframe)

    def get_eqhl(self,timeframe)->list[Level]:
        with self._lock:
            return self._eqhl[timeframe]

    def get_swings(self,timeframe)->list[PDArray]:
        with self._lock:
            return self._swings[timeframe]

    def get_current_structure(self,timeframe)->list[Structure]:
        with self._lock:
            return [self._current_mss[timeframe],self._current_bos[timeframe],self._current_cisd[timeframe]]

    def get_previous_structure(self,timeframe)->list[Structure]:
        with self._lock:
            return [self._previous_mss[timeframe],self._previous_bos]

    def clear(self):
        self._swings.clear()
        self._consecutive_candles.clear()
        self._current_mss.clear()
        self._previous_mss.clear()
        self._current_bos.clear()
        self._previous_bos.clear()
        self._current_cisd.clear()
        self._bos.clear()
        self._eqhl.clear()
        self._cisd.clear()

    def _detect_swing(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Swing patterns."""
        swing = Swing.detect_swing(first_candle, second_candle, third_candle)
        if swing:
            if timeframe not in self._swings:
                self._swings[timeframe] = []
            self._swings[timeframe].append(swing)

    def _detect_eqhl(self, timeframe: int, atr:float):
        """Detects EQHL patterns."""
        if timeframe in self._swings:
            swings = self._swings[timeframe]
            eqhl = equalHL().detect_equal_hl(swings=swings, adr=atr)
            if eqhl:
                if timeframe not in self._eqhl:
                    self._eqhl[timeframe] = []
                self._eqhl[timeframe].extend(eqhl)

    def _detect_mss(self, third_candle: Candle, timeframe: int):
        if timeframe in self._swings:
            for swing in self._swings[timeframe]:
                swing: PDArray
                mss = MSS.detect_mss(last_candle=third_candle, swing=swing)
                if mss:
                    if timeframe not in self._previous_mss:
                        self._previous_mss[timeframe] = mss
                    if timeframe not in self._current_mss:
                        self._current_mss[timeframe] = mss

                    self._previous_mss[timeframe] = self._current_mss[timeframe]
                    self._current_mss[timeframe] = mss
                    if mss.invalidation_candle is None:
                        swing.status = "Sweeped"
                        mss.invalidation_candle = third_candle
                    break

    def _detect_bos(self, third_candle: Candle, timeframe: int):
        if timeframe not in self._bos:
            self._bos[timeframe] = BOS()
        bos = self._bos[timeframe].detect_bos(last_candle=third_candle)
        if bos:
            if timeframe not in self._current_bos:
                self._current_bos[timeframe] = bos
            if timeframe not in self._previous_bos:
                self._previous_bos[timeframe] = self._current_bos[timeframe]

            self._previous_bos[timeframe] = self._current_bos[timeframe]
            self._current_bos[timeframe] = bos

    def _detect_consecutive(self, third_candle: Candle, timeframe: int):
        if timeframe not in self._cisd:
            self._cisd[timeframe] = CISD()
        if timeframe not in self._consecutive_candles:
            self._consecutive_candles[timeframe] = []
        consecutive = self._cisd[timeframe].add_candle(last_candle=third_candle)
        if consecutive:
            self._consecutive_candles[timeframe].append(consecutive)

    def _detect_cisd(self, third_candle: Candle, timeframe: int):
        if timeframe in self._consecutive_candles[timeframe] and timeframe in self._cisd and timeframe in \
                self._current_cisd[timeframe]:
            for consecutive_candle in self._consecutive_candles[timeframe]:
                cisd: Structure = self._cisd[timeframe].check_for_cisd(third_candle, consecutive_candle)
                if cisd:
                    self._current_cisd[timeframe] = cisd
                    if cisd.invalidation_candle is None:
                        cisd.invalidation_candle = third_candle

    def _detect_choch(self, timeframe: int):
        if timeframe in self._current_bos and timeframe in self._previous_bos:
            if Choch.is_choch(current_bos=self._current_bos[timeframe]
                    , previous_bos=self._previous_bos[timeframe]):
                self._current_bos[timeframe].status = "CHOCH"

    def _detect_liquidity_sweep(self, third_candle: Candle, timeframe: int):
        if timeframe in self._swings:
            for swing in self._swings[timeframe]:
                if Swing.detect_sweep(last_candle=third_candle, swing=swing):
                    swing.status = "Sweeped"
                    if swing.invalidation_candle is None:
                        swing.invalidation_candle = third_candle

    def _detect_mitigation_block(self, timeframe: int):
        if timeframe in self._current_bos and timeframe in self._current_mss:
            if MitigationBlock.is_mitigated(self._current_mss[timeframe], self._current_bos[timeframe]):
                self._current_bos[timeframe].status = "MITIGATED"

    def remove_duplicates(self,timeframe: int):
        self._remove_duplicate_swings(timeframe)
        self._remove_duplicate_consecutive_candles(timeframe)
        self._remove_duplicate_eqhl(timeframe)

    def remove_by_ids(self, _ids: list, timeframe: int):
        self._remove_swings_by_ids(_ids, timeframe)
        self._remove_consecutive_candles_by_ids(_ids, timeframe)
        self._remove_eqhls_by_ids(_ids, timeframe)


    def _remove_swings_by_ids(self, _ids, timeframe):
        self._swings[timeframe] = [
            swing for swing in self._swings[timeframe]
            if all(candle.id in _ids for candle in swing.candles)
        ]

    def _remove_duplicate_swings(self, timeframe: int):
        if timeframe not in self._swings:
            return

        unique_eqhl = []
        seen_candle_sets = set()  # Track unique sets of candle IDs

        for hl in self._swings[timeframe]:
            if hl._name == "High" or hl._name == "Low":
                candle_ids = frozenset(candle.id for candle in hl.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_eqhl.append(hl)
                    seen_candle_sets.add(candle_ids)  # Mark as seen

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._swings[timeframe] = unique_eqhl

    def _remove_consecutive_candles_by_ids(self, _ids, timeframe):
        self._consecutive_candles[timeframe] = [consecutive for consecutive in self._consecutive_candles[timeframe]
                                 if all(candle.id in _ids for candle in consecutive.candles)]

    def _remove_duplicate_consecutive_candles(self, timeframe: int):
        if timeframe not in self._consecutive_candles:
            return

        unique_consecutive_candles = []  # Stores filtered consecutive candle groups
        seen_candle_sets = set()  # Tracks existing sets of candle IDs

        # Sort by length to ensure we keep the longest first
        sorted_candle_groups = sorted(self._consecutive_candles[timeframe], key=lambda x: len(x.candles), reverse=True)

        for consecutive_candles in sorted_candle_groups:
            candle_ids = frozenset(candle.id for candle in consecutive_candles.candles)  # Extract candle IDs

            # If no subset of these candles is already stored, keep it
            if not any(existing_ids.issubset(candle_ids) for existing_ids in seen_candle_sets):
                unique_consecutive_candles.append(consecutive_candles)
                seen_candle_sets.add(candle_ids)  # Add to tracking set

        # Update the list with filtered consecutive candles
        self._consecutive_candles[timeframe] = unique_consecutive_candles

    def _remove_eqhls_by_ids(self, _ids, timeframe):
        self._eqhl[timeframe] = [eqhl for eqhl in self._eqhl[timeframe]
                                 if all(candle.id in _ids for candle in eqhl.candles)]


    def _remove_duplicate_eqhl(self, timeframe: int):
        if timeframe not in self._eqhl:
            return

        unique_eqhl = []
        seen_candle_sets = set()  # Track unique sets of candle IDs

        for hl in self._eqhl[timeframe]:
            if hl._name == "EQH" or hl._name == "EQL":
                candle_ids = frozenset(candle.id for candle in hl.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_eqhl.append(hl)
                    seen_candle_sets.add(candle_ids)  # Mark as seen

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._eqhl[timeframe] = unique_eqhl