import threading

from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.pdarray.imbalance.BPR import BPR
from files.models.frameworks.pdarray.imbalance.FVG import FVG
from files.models.frameworks.pdarray.imbalance.IFVG import IFVG
from files.models.frameworks.pdarray.imbalance.ImbalanceStatusEnum import ImbalanceStatusEnum
from files.models.frameworks.pdarray.imbalance.InversionFVG import InversionFVG
from files.models.frameworks.pdarray.imbalance.Void import Void
from files.models.frameworks.pdarray.imbalance.VolumeImbalance import VolumeImbalance


class ImbalanceMediator:
    def __init__(self):
        self._lock = threading.Lock()
        self._imbalances: dict[int, list[PDArray]] = {}

    def analyze(self,first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe):
        with self._lock:
            self._detect_fvg(first_candle, second_candle, third_candle, timeframe)
            self._detect_ifvg(first_candle, second_candle, third_candle, timeframe)
            self._detect_void(second_candle, third_candle, timeframe)
            self._detect_volume_imbalance(second_candle, third_candle, timeframe)
            self._detect_bpr(timeframe)

            self._detect_inversion_fvg(third_candle, timeframe)

            self._remove_duplicate_bpr(timeframe)

    def clear(self):
        self._imbalances.clear()

    def get_imbalances(self, timeframe: int) -> list[PDArray]:
        """Returns the imbalances for a given timeframe."""
        return self._imbalances[timeframe]

    def _detect_fvg(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects FVG patterns."""
        fvg = FVG.detect_fvg(first_candle=first_candle, second_candle=second_candle, third_candle=third_candle)

        if fvg:
            if timeframe not in self._imbalances:
                self._imbalances[timeframe] = []
            self._imbalances[timeframe].append(fvg)

    def _detect_ifvg(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects FVG patterns."""
        ifvg = IFVG.detect_ifvg(first_candle=first_candle, second_candle=second_candle, third_candle=third_candle)

        if ifvg:
            if timeframe not in self._imbalances:
                self._imbalances[timeframe] = []
            self._imbalances[timeframe].append(ifvg)

    def _detect_void(self, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Void patterns."""
        void = Void.detect_void(first_candle=second_candle, second_candle=third_candle)

        if void:
            if timeframe not in self._imbalances:
                self._imbalances[timeframe] = []
            self._imbalances[timeframe].append(void)

    def _detect_volume_imbalance(self, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Void patterns."""
        void = VolumeImbalance.detect_volume_imbalance(first_candle=second_candle, second_candle=third_candle)
        if void:
            if timeframe not in self._imbalances:
                self._imbalances[timeframe] = []
            self._imbalances[timeframe].append(void)

    def _detect_bpr(self, timeframe: int):
        """Detects BPR patterns."""
        if timeframe in self._imbalances:
            for imbalance in self._imbalances[timeframe]:
                buy_fvg = None
                sell_fvg = None
                if imbalance._name == "FVG":
                    if imbalance.direction == "Bullish":
                        buy_fvg = imbalance
                    if imbalance.direction == "Bearish":
                        sell_fvg = imbalance
                else:
                    continue
                for imbalance2 in self._imbalances[timeframe]:
                    if imbalance2._name == imbalance._name and imbalance2.direction != imbalance.direction:
                        if imbalance2.direction == "Bullish":
                            buy_fvg = imbalance2
                        if imbalance2.direction == "Bearish":
                            sell_fvg = imbalance2
                        bpr = BPR.detect_bpr(buy_fvg, sell_fvg)
                        if bpr:
                            if timeframe not in self._imbalances:
                                self._imbalances[timeframe] = []
                            self._imbalances[timeframe].append(bpr)

    def _detect_inversion_fvg(self, third_candle: Candle, timeframe: int):
        if timeframe in self._imbalances:
            for imbalance in self._imbalances[timeframe]:
                if imbalance._name == "FVG" or imbalance._name == "IFVG":
                    if InversionFVG.detect_inversion(last_candle=third_candle, fvg=imbalance):
                        if imbalance.status == ImbalanceStatusEnum.Normal.value or imbalance.status == ImbalanceStatusEnum.Reclaimed.value:
                            imbalance.status = ImbalanceStatusEnum.Inversed.value
                            if imbalance.invalidation_candle is None:
                                imbalance.invalidation_candle = third_candle
                    else:
                        if imbalance.status == ImbalanceStatusEnum.Inversed.value:
                            imbalance.status = ImbalanceStatusEnum.Reclaimed.value

    def remove_imbalances_by_ids(self, _ids, timeframe):
        self._imbalances[timeframe] = [imbalances for imbalances in self._imbalances[timeframe]
                                 if all(candle.id in _ids for candle in imbalances.candles)]


    def _remove_duplicate_bpr(self, timeframe: int):
        if timeframe not in self._imbalances:
            return

        unique_bpr_candles = []
        seen_candle_sets = set()  # Track unique sets of candle IDs
        non_bpr_imbalances = []  # Store non-BPR imbalances

        for imbalance in self._imbalances[timeframe]:
            if imbalance._name == "BPR" or imbalance._name == "IFVG" or imbalance._name == "FVG":
                candle_ids = frozenset(candle.id for candle in imbalance.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_bpr_candles.append(imbalance)
                    seen_candle_sets.add(candle_ids)  # Mark as seen
            else:
                non_bpr_imbalances.append(imbalance)  # Keep non-BPR imbalances

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._imbalances[timeframe] = unique_bpr_candles + non_bpr_imbalances
