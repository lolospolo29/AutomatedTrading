import threading
from typing import Optional

from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.frameworks.Structure import Structure
from app.models.frameworks.level.ADR import ADR
from app.models.frameworks.pdarray.Swing import Swing
from app.models.frameworks.pdarray.imbalance.BPR import BPR
from app.models.frameworks.pdarray.imbalance.FVG import FVG
from app.models.frameworks.pdarray.imbalance.IFVG import IFVG
from app.models.frameworks.pdarray.imbalance.ImbalanceStatusEnum import ImbalanceStatusEnum
from app.models.frameworks.pdarray.imbalance.InversionFVG import InversionFVG
from app.models.frameworks.pdarray.imbalance.Void import Void
from app.models.frameworks.pdarray.imbalance.VolumeImbalance import VolumeImbalance
from app.models.frameworks.pdarray.opens.NDOG import NDOG
from app.models.frameworks.pdarray.opens.NWOG import NWOG
from app.models.frameworks.pdarray.orderblock.Breaker import Breaker
from app.models.frameworks.pdarray.orderblock.OrderBlock import Orderblock
from app.models.frameworks.pdarray.orderblock.OrderBlockStatusEnum import OrderBlockStatusEnum
from app.models.frameworks.pdarray.orderblock.PB import PB
from app.models.frameworks.pdarray.orderblock.RejectionBlock import RejectionBlock
from app.models.frameworks.pdarray.orderblock.SCOB import SCOB
from app.models.frameworks.structure.BOS import BOS
from app.models.frameworks.structure.CISD import CISD
from app.models.frameworks.structure.Choch import Choch
from app.models.frameworks.structure.MSS import MSS


class PriceMediator:
    def __init__(self):
        self._lock = threading.Lock()
        self._candles: dict[int, list[Candle]] = {}
        self._swings: dict[int, list[PDArray]] = {}
        self._imbalances: dict[int, list[PDArray]] = {}
        self._orderblocks: dict[int, list[PDArray]] = {}
        self._probulsion_blocks: dict[str, list[PDArray]] = {}
        self._consecutive_candles: dict[int, list[Structure]] = {}
        self._current_mss: dict[int, Structure] = {}
        self._previous_mss: dict[int, Structure] = {}
        self._current_bos: dict[int, Structure] = {}
        self._previous_bos: dict[int, Structure] = {}
        self._current_cisd: dict[int, Structure] = {}
        self._current_choch: dict[int, bool] = {}
        self._bos: dict[int, Structure] = {}
        self._cisd: dict[int, Structure] = {}
        self._ndog: list[PDArray] = []
        self._nwog: list[PDArray] = []
        self._adr: float = 0.0

    def add_candle(self, candle: Candle):
        with self._lock:
            if candle.timeframe not in self._candles:
                self._candles[candle.timeframe] = []
            self._candles[candle.timeframe].append(candle)

    def detect_pd_arrays(self, timeframe: int):
        with self._lock:
            if len(self._candles[timeframe]) >= 3:
                first_candle, second_candle, third_candle = self._candles[timeframe][-3:]

                # Execute each detection step in order

                # Openings
                self._detect_ndog(second_candle, third_candle)
                self._detect_nwog(second_candle, third_candle)

                # Orderblocks and Swing

                self._detect_swing(first_candle, second_candle, third_candle, timeframe)
                self._detect_orderblock(second_candle, third_candle, timeframe)
                self._detect_scob(first_candle, second_candle, third_candle, timeframe)
                self._detect_rejection_block(third_candle, timeframe)
                self._detect_probulsion(third_candle, timeframe)

                # Imbalance

                self._detect_fvg(first_candle, second_candle, third_candle, timeframe)
                self._detect_ifvg(first_candle, second_candle, third_candle, timeframe)
                self._detect_void(second_candle, third_candle, timeframe)
                self._detect_volume_imbalance(second_candle, third_candle, timeframe)
                self._detect_bpr(timeframe)

                # Structure

                self._detect_mss(third_candle, timeframe)
                self._detect_bos(third_candle, timeframe)
                self._detect_consecutive(third_candle, timeframe)
                self._detect_choch(timeframe)

                # Status Change

                self._detect_breaker(third_candle, timeframe)
                self._detect_inversion_fvg(third_candle, timeframe)

    # ---- Getter Methods ---- #

    def get_candles(self, key: int) -> list[Candle]:
        """Returns the list of candles for a given timeframe."""
        return self._candles.get(key, [])

    def get_swings(self, key: int) -> list[PDArray]:
        """Returns the swings for a given timeframe."""
        return self._swings.get(key, [])

    def get_imbalances(self, key: int) -> list[PDArray]:
        """Returns the imbalances for a given timeframe."""
        return self._imbalances.get(key, [])

    def get_orderblocks(self, key: int) -> list[PDArray]:
        """Returns the orderblocks for a given timeframe."""
        return self._orderblocks.get(key, [])

    def get_probulsion_blocks(self, key: str) -> list[PDArray]:
        """Returns the propulsion blocks based on their ID."""
        return self._probulsion_blocks.get(key, [])

    def get_consecutive_candles(self, key: int) -> list[Structure]:
        """Returns consecutive candles for a given timeframe."""
        return self._consecutive_candles.get(key, [])

    def get_mss(self, key: int, previous: bool = False) -> Optional[Structure]:
        """Returns the current or previous MSS for a given timeframe."""
        return self._previous_mss.get(key) if previous else self._current_mss.get(key)

    def get_bos(self, key: int, previous: bool = False) -> Optional[Structure]:
        """Returns the current or previous BOS for a given timeframe."""
        return self._previous_bos.get(key) if previous else self._current_bos.get(key)

    def get_cisd(self, key: int) -> Optional[Structure]:
        """Returns the CISD for a given timeframe."""
        return self._cisd.get(key)

    def get_choch(self, key: int) -> Optional[bool]:
        """Returns the CHoCH (Change of Character) for a given timeframe."""
        return self._current_choch.get(key)

    def get_ndog(self) -> list[PDArray]:
        """Returns the NDOG patterns detected."""
        return self._ndog

    def get_nwog(self) -> list[PDArray]:
        """Returns the NWOG patterns detected."""
        return self._nwog

    def get_adr(self) -> float:
        """Returns the current ADR (Average Daily Range)."""
        return self._adr

    def reset(self):
        with self._lock:
            self._candles.clear()
            self._swings.clear()
            self._imbalances.clear()
            self._orderblocks.clear()
            self._probulsion_blocks.clear()
            self._consecutive_candles.clear()
            self._current_mss.clear()
            self._previous_mss.clear()
            self._current_bos.clear()
            self._previous_bos.clear()
            self._current_cisd.clear()
            self._current_choch.clear()
            self._bos.clear()
            self._cisd.clear()
            self._ndog.clear()
            self._nwog.clear()
            self._adr = 0.0

    def get_current_adr(self, timeframe) -> float:
        self._calculate_average_range(timeframe)
        return self._adr

    # ---- Modular detection methods ---- #

    def _calculate_average_range(self, timeframe: int):
        candles = self._candles[timeframe]
        high = max(candle.high for candle in candles)
        low = min(candle.low for candle in candles)
        self._adr = ADR.calculate_adr(high, low)

    def _detect_ndog(self, second_candle: Candle, third_candle: Candle):
        """Detects NDOG patterns."""
        ndog = NDOG.detect_ndog(first_candle=second_candle, second_candle=third_candle)
        self._ndog.append(ndog)

    def _detect_nwog(self, second_candle: Candle, third_candle: Candle):
        """Detects NWOG patterns."""
        nwog = NWOG.detect_nwog(first_candle=second_candle, second_candle=third_candle)
        self._nwog.append(nwog)

    def _detect_swing(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Swing patterns."""
        swing = Swing.detect_swing(first_candle, second_candle, third_candle)
        if swing:
            if timeframe not in self._swings:
                self._swings[timeframe] = []
            self._swings[timeframe].append(swing)

    def _detect_orderblock(self, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Orderblock patterns."""
        orderblock = Orderblock.return_orderblock(first_candle=second_candle, second_candle=third_candle)
        if orderblock:
            if timeframe not in self._orderblocks:
                self._orderblocks[timeframe] = []
            self._orderblocks[timeframe].append(orderblock)

    def _detect_scob(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects SCOB patterns."""
        scob = SCOB.detect_pd_single_candle_ob(first_candle=first_candle, second_candle=second_candle,
                                               third_candle=third_candle)
        if scob:
            if timeframe not in self._orderblocks:
                self._orderblocks[timeframe] = []
            self._orderblocks[timeframe].append(scob)

    def _detect_rejection_block(self, third_candle: Candle, timeframe: int):
        """Detects rejection patterns."""
        rejection_block = RejectionBlock.detect_rejection_block(candle=third_candle,
                                                                average_range=self.get_current_adr(timeframe))

        if rejection_block:
            if timeframe not in self._orderblocks:
                self._orderblocks[timeframe] = []
            self._orderblocks[timeframe].append(rejection_block)

    def _detect_probulsion(self, third_candle: Candle, timeframe: int):
        """Detects probulsion patterns."""
        for orderblock in self._orderblocks[timeframe]:
            if orderblock.name == "OB" or orderblock.name == "SCOB":
                pb = PB.detect_probulsion_block(last_candle=third_candle, orderblock=orderblock)
                if pb:
                    if timeframe not in self._probulsion_blocks:
                        self._probulsion_blocks[pb.reference_pd] = []
                    self._probulsion_blocks[pb.reference_pd].append(pb)

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
        for imbalance in self._imbalances[timeframe]:
            buy_fvg = None
            sell_fvg = None
            if imbalance.name == "FVG" and imbalance.direction == "Bullish":
                buy_fvg = imbalance
            if imbalance.name == "FVG" and imbalance.direction == "Bearish":
                sell_fvg = imbalance
            for imbalance2 in self._imbalances[timeframe]:
                if imbalance2.name == imbalance.name and imbalance2.direction != imbalance.direction:
                    if imbalance2.direction == "Bullish":
                        buy_fvg = imbalance2
                    if imbalance2.direction == "Bearish":
                        sell_fvg = imbalance2
                    bpr = BPR.detect_bpr(buy_fvg, sell_fvg)
                    if bpr:
                        if timeframe not in self._imbalances:
                            self._imbalances[timeframe] = []
                        self._imbalances[timeframe].append(bpr)

    def _detect_mss(self, third_candle: Candle, timeframe: int):
        for swing in self._swings[timeframe]:
            swing: PDArray
            mss = MSS.detect_mss(last_candle=third_candle, swing=swing)
            if mss:
                if timeframe not in self._current_mss:
                    self._current_mss[timeframe] = []
                if timeframe not in self._current_mss:
                    self._previous_mss[timeframe] = []

                self._previous_mss[timeframe] = self._current_mss[timeframe]
                self._current_mss[timeframe] = mss
                swing.status = "Sweeped"
                break

    def _detect_bos(self, third_candle: Candle, timeframe: int):
        if timeframe not in self._bos:
            self._bos[timeframe] = BOS()
        bos = self._bos[timeframe].detect_bos(third_candle=third_candle)
        if bos:
            if timeframe not in self._current_bos:
                self._current_bos[timeframe] = []
            if timeframe not in self._previous_bos:
                self._previous_bos[timeframe] = []
            self._previous_bos[timeframe] = self._current_bos[timeframe]
            self._current_bos[timeframe] = bos

    def _detect_consecutive(self, third_candle: Candle, timeframe: int):
        if timeframe not in self._cisd:
            self._cisd[timeframe] = CISD()
        consecutive = self._cisd[timeframe].add_candle(third_candle=third_candle)
        if consecutive:
            if timeframe not in self._consecutive_candles:
                self._consecutive_candles[timeframe] = []
            self._consecutive_candles[timeframe].append(consecutive)

        for consecutive_candle in self._cisd[timeframe]:
            cisd = self._cisd[timeframe].check_for_cisd(third_candle=third_candle,
                                                        consecutive_candle=consecutive_candle)
            if cisd:
                self._consecutive_candles[timeframe] = cisd

    def _detect_choch(self, timeframe: int):
        if timeframe in self._current_bos and timeframe in self._previous_bos:
            self._current_choch[timeframe] = Choch.is_choch(current_bos=self._current_bos[timeframe]
                                                            , previous_bos=self._previous_bos[timeframe])

    def _detect_breaker(self, third_candle: Candle, timeframe: int):
        for orderblock in self._orderblocks[timeframe]:
            if orderblock.name == "OB" or orderblock.name == "SCOB":
                breaker = Breaker.detect_breaker(last_candle=third_candle, orderblock=orderblock)
                if breaker:
                    orderblock.status = OrderBlockStatusEnum.Breaker.value
                if not breaker:
                    orderblock.status = OrderBlockStatusEnum.Normal.value

    def _detect_inversion_fvg(self, third_candle: Candle, timeframe: int):
        for imbalance in self._imbalances[timeframe]:
            if imbalance.name == "FVG" or imbalance.name == "IFVG":
                if InversionFVG.detect_inversion(last_candle=third_candle, fvg=imbalance):
                    if imbalance.status == ImbalanceStatusEnum.Normal.value or imbalance.status == ImbalanceStatusEnum.Reclaimed.value:
                        imbalance.status = ImbalanceStatusEnum.Inversed.value
                else:
                    if imbalance.status == ImbalanceStatusEnum.Inversed.value:
                        imbalance.status = ImbalanceStatusEnum.Reclaimed.value
