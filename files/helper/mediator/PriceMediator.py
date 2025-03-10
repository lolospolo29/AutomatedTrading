import threading
from typing import Optional

from files.interfaces.ITimeWindow import ITimeWindow
from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from files.models.frameworks.level.ADR import ADR
from files.models.frameworks.level.Fibonnaci import Fibonnaci
from files.models.frameworks.level.PreviousSessionLevels import PreviousSessionLevels
from files.models.frameworks.level.equalHL import equalHL
from files.models.frameworks.pdarray.Swing import Swing
from files.models.frameworks.pdarray.imbalance.BPR import BPR
from files.models.frameworks.pdarray.imbalance.FVG import FVG
from files.models.frameworks.pdarray.imbalance.IFVG import IFVG
from files.models.frameworks.pdarray.imbalance.ImbalanceStatusEnum import ImbalanceStatusEnum
from files.models.frameworks.pdarray.imbalance.InversionFVG import InversionFVG
from files.models.frameworks.pdarray.imbalance.Void import Void
from files.models.frameworks.pdarray.imbalance.VolumeImbalance import VolumeImbalance
from files.models.frameworks.pdarray.opens.NDOG import NDOG
from files.models.frameworks.pdarray.opens.NWOG import NWOG
from files.models.frameworks.pdarray.orderblock.Breaker import Breaker
from files.models.frameworks.pdarray.orderblock.OrderBlock import Orderblock
from files.models.frameworks.pdarray.orderblock.OrderBlockStatusEnum import OrderBlockStatusEnum
from files.models.frameworks.pdarray.orderblock.PB import PB
from files.models.frameworks.pdarray.orderblock.RejectionBlock import RejectionBlock
from files.models.frameworks.pdarray.orderblock.SCOB import SCOB
from files.models.frameworks.structure.BOS import BOS
from files.models.frameworks.structure.CISD import CISD
from files.models.frameworks.structure.Choch import Choch
from files.models.frameworks.structure.MSS import MSS
from files.models.frameworks.structure.MitigationBlock import MitigationBlock

class PriceMediator:
    def __init__(self):
        self._lock = threading.Lock()
        self._ote = Fibonnaci([0.62,0.705,1.5],"OTE")
        self._pd = Fibonnaci([0.0,0.5,1.0],"PD")
        self._deviation = Fibonnaci([1.5,2.0,3.0,4.0],"STDV")
        self._swings: dict[int, list[PDArray]] = {}
        self._eqhl: dict[int, list[Level]] = {}
        self._imbalances: dict[int, list[PDArray]] = {}
        self._orderblocks: dict[int, list[PDArray]] = {}
        self._probulsion_blocks: dict[str, list[PDArray]] = {}
        self._consecutive_candles: dict[int, list[Structure]] = {}
        self._current_mss: dict[int, Structure] = {}
        self._previous_mss: dict[int, Structure] = {}
        self._current_bos: dict[int, Structure] = {}
        self._previous_bos: dict[int, Structure] = {}
        self._current_cisd: dict[int, Structure] = {}
        self._bos: dict[int, Structure] = {}
        self._cisd: dict[int, Structure] = {}
        self._ndog: list[PDArray] = []
        self._nwog: list[PDArray] = []
        self._adr: float = 0.0

    def detect_pd_arrays(self, first_candle:Candle, second_candle:Candle, third_candle:Candle, timeframe):
        with self._lock:

            # ADR

            self._calculate_average_range(first_candle, second_candle, third_candle)

            # Openings

            self._detect_ndog(second_candle, third_candle)
            self._detect_nwog(second_candle, third_candle)

            # Orderblocks and Swing

            self._detect_swing(first_candle, second_candle, third_candle, timeframe)
            self._detect_eqhl(timeframe)
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
            self._detect_cisd(third_candle, timeframe)

            # Status Change

            self._detect_choch(timeframe)
            self._detect_breaker(third_candle, timeframe)
            self._detect_inversion_fvg(third_candle, timeframe)
            self._detect_liquidity_sweep(third_candle, timeframe)
            self._detect_mitigation_block(timeframe)

            # Remove Duplicates

            self._remove_duplicate_consecutive_candles(timeframe)
            self._remove_duplicate_bpr(timeframe)
            self._remove_duplicate_eqhl(timeframe)
            self._remove_duplicate_orderblocks(timeframe)
            self._remove_duplicate_consecutive_candles(timeframe)
            self._remove_duplicate_swings(timeframe)

    # region ---- Getter Methods ----

    @staticmethod
    def get_previous_session_hl(candles:list[Candle],time_window: ITimeWindow) -> list[Level]:
        return PreviousSessionLevels.return_levels(candles, time_window)

    def get_fibonnaci(self,candles:list[Candle],ote:bool=True,pd:bool=False,stdv:bool=False,fib_levels:list[float]=None) -> list[Level]:
        highest_candle = max(candles, key=lambda candle: candle.high)
        lowest_candle = min(candles, key=lambda candle: candle.low)

        if fib_levels:
            return Fibonnaci(fib_levels,"User").return_levels(highest_candle, lowest_candle)
        if stdv:
            return self._deviation.return_levels(highest_candle, lowest_candle)
        if pd:
            return self._pd.return_levels(highest_candle, lowest_candle)
        if ote:
            return self._ote.return_levels(highest_candle, lowest_candle)

    def get_swings(self, timeframe: int) -> list[PDArray]:
        """Returns the swings for a given timeframe."""
        return self._swings.get(timeframe, [])

    def get_eqhl(self, timeframe: int) -> list[Level]:
        """Returns the swings for a given timeframe."""
        return self._eqhl.get(timeframe, [])

    def get_imbalances(self, timeframe: int) -> list[PDArray]:
        """Returns the imbalances for a given timeframe."""
        return self._imbalances.get(timeframe, [])

    def get_orderblocks(self, timeframe: int) -> list[PDArray]:
        """Returns the orderblocks for a given timeframe."""
        return self._orderblocks.get(timeframe, [])

    def get_probulsion_blocks(self, timeframe: str) -> list[PDArray]:
        """Returns the propulsion blocks based on their ID."""
        return self._probulsion_blocks.get(timeframe, [])

    def get_consecutive_candles(self, timeframe: int) -> list[Structure]:
        """Returns consecutive candles for a given timeframe."""
        return self._consecutive_candles.get(timeframe, [])

    def get_mss(self, timeframe: int, previous: bool = False) -> Optional[Structure]:
        """Returns the current or previous MSS for a given timeframe."""
        return self._previous_mss.get(timeframe) if previous else self._current_mss.get(timeframe)

    def get_bos(self, timeframe: int, previous: bool = False) -> Optional[Structure]:
        """Returns the current or previous BOS for a given timeframe."""
        return self._previous_bos.get(timeframe) if previous else self._current_bos.get(timeframe)

    def get_cisd(self, timeframe: int) -> Optional[Structure]:
        """Returns the CISD for a given timeframe."""
        return self._current_cisd.get(timeframe)

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
            self._bos.clear()
            self._eqhl.clear()
            self._cisd.clear()
            self._adr = 0.0

    def get_current_adr(self) -> float:
        return self._adr

    # endregion

    # region ---- Modular detection methods ----
    def _calculate_average_range(self,first_candle:Candle, second_candle:Candle, third_candle:Candle):
        high = max(first_candle.high, second_candle.high, third_candle.high)
        low = min(first_candle.high, second_candle.high, third_candle.high)
        if self._adr == 0:
            self._adr = ADR.calculate_adr(high, low)
        else:
            self._adr = (self._adr + ADR.calculate_adr(high, low)) / 2

    def _detect_ndog(self, second_candle: Candle, third_candle: Candle):
        """Detects NDOG patterns."""
        ndog = NDOG.detect_ndog(first_candle=second_candle, second_candle=third_candle)
        if ndog:
            self._ndog.append(ndog)

    def _detect_nwog(self, second_candle: Candle, third_candle: Candle):
        """Detects NWOG patterns."""
        nwog = NWOG.detect_nwog(first_candle=second_candle, second_candle=third_candle)
        if nwog:
            self._nwog.append(nwog)

    def _detect_swing(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe: int):
        """Detects Swing patterns."""
        swing = Swing.detect_swing(first_candle, second_candle, third_candle)
        if swing:
            if timeframe not in self._swings:
                self._swings[timeframe] = []
            self._swings[timeframe].append(swing)

    def _detect_eqhl(self, timeframe: int):
        """Detects EQHL patterns."""
        if timeframe in self._swings:
            swings = self._swings[timeframe]
            eqhl = equalHL().detect_equal_hl(swings=swings, adr=self._adr)
            if eqhl:
                if timeframe not in self._eqhl:
                    self._eqhl[timeframe] = []
                self._eqhl[timeframe].extend(eqhl)

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
                                                                average_range=self.get_current_adr())

        if rejection_block:
            if timeframe not in self._orderblocks:
                self._orderblocks[timeframe] = []
            self._orderblocks[timeframe].append(rejection_block)

    def _detect_probulsion(self, third_candle: Candle, timeframe: int):
        """Detects probulsion patterns."""
        if timeframe in self._orderblocks:
            for orderblock in self._orderblocks[timeframe]:
                if orderblock.name == "OB" or orderblock.name == "SCOB":
                    pb = PB.detect_probulsion_block(last_candle=third_candle, orderblock=orderblock)
                    if pb:
                        pb.reference = orderblock.id
                        if timeframe not in self._probulsion_blocks:
                            self._probulsion_blocks[pb.reference] = []
                        self._probulsion_blocks[pb.reference].append(pb)

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
                if imbalance.name == "FVG":
                    if imbalance.direction == "Bullish":
                        buy_fvg = imbalance
                    if imbalance.direction == "Bearish":
                        sell_fvg = imbalance
                else:
                    continue
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
                cisd:Structure = self._cisd[timeframe].check_for_cisd(third_candle, consecutive_candle)
                if cisd:
                    self._current_cisd[timeframe] = cisd
                    if cisd.invalidation_candle is None:
                        cisd.invalidation_candle = third_candle

    def _detect_choch(self, timeframe: int):
        if timeframe in self._current_bos and timeframe in self._previous_bos:
            if Choch.is_choch(current_bos=self._current_bos[timeframe]
                    , previous_bos=self._previous_bos[timeframe]):
                self._current_bos[timeframe].status = "CHOCH"

    def _detect_breaker(self, third_candle: Candle, timeframe: int):
        if timeframe in self._orderblocks:
            for orderblock in self._orderblocks[timeframe]:
                if orderblock.name == "OB" or orderblock.name == "SCOB":
                    breaker = Breaker.detect_breaker(last_candle=third_candle, orderblock=orderblock)
                    if breaker:
                        orderblock.status = OrderBlockStatusEnum.Breaker.value
                        if orderblock.invalidation_candle is None:
                            orderblock.invalidation_candle = third_candle
                    if not breaker:
                        if orderblock == OrderBlockStatusEnum.Breaker.value:
                            orderblock.status = OrderBlockStatusEnum.Reclaimed.value
                        else:
                            orderblock.status = OrderBlockStatusEnum.Normal.value

    def _detect_inversion_fvg(self, third_candle: Candle, timeframe: int):
        if timeframe in self._imbalances:
            for imbalance in self._imbalances[timeframe]:
                if imbalance.name == "FVG" or imbalance.name == "IFVG":
                    if InversionFVG.detect_inversion(last_candle=third_candle, fvg=imbalance):
                        if imbalance.status == ImbalanceStatusEnum.Normal.value or imbalance.status == ImbalanceStatusEnum.Reclaimed.value:
                            imbalance.status = ImbalanceStatusEnum.Inversed.value
                            if imbalance.invalidation_candle is None:
                                imbalance.invalidation_candle = third_candle
                    else:
                        if imbalance.status == ImbalanceStatusEnum.Inversed.value:
                            imbalance.status = ImbalanceStatusEnum.Reclaimed.value

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

    # endregion
    def _remove_duplicate_swings(self, timeframe: int):
        if timeframe not in self._swings:
            return

        unique_eqhl = []
        seen_candle_sets = set()  # Track unique sets of candle IDs

        for hl in self._swings[timeframe]:
            if hl.name == "High" or hl.name == "Low":
                candle_ids = frozenset(candle.id for candle in hl.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_eqhl.append(hl)
                    seen_candle_sets.add(candle_ids)  # Mark as seen

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._swings[timeframe] = unique_eqhl

    def _remove_duplicate_eqhl(self, timeframe: int):
        if timeframe not in self._eqhl:
            return

        unique_eqhl = []
        seen_candle_sets = set()  # Track unique sets of candle IDs

        for hl in self._eqhl[timeframe]:
            if hl.name == "EQH" or hl.name == "EQL":
                candle_ids = frozenset(candle.id for candle in hl.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_eqhl.append(hl)
                    seen_candle_sets.add(candle_ids)  # Mark as seen

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._eqhl[timeframe] = unique_eqhl

    def _remove_duplicate_pbs(self, timeframe: int):
        if timeframe not in self._probulsion_blocks:
            return

        unique_ob = []
        seen_candle_sets = set()  # Track unique sets of candle IDs
        non_obs = []  # Store non-BPR imbalances

        for pb in self._probulsion_blocks[timeframe]:
            if pb.name == "PB":
                candle_ids = frozenset(candle.id for candle in pb.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_ob.append(pb)
                    seen_candle_sets.add(candle_ids)  # Mark as seen
            else:
                non_obs.append(pb)  # Keep non-BPR imbalances

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._probulsion_blocks[timeframe] = unique_ob + non_obs


    def _remove_duplicate_orderblocks(self, timeframe: int):
        if timeframe not in self._orderblocks:
            return

        unique_ob = []
        seen_candle_sets = set()  # Track unique sets of candle IDs
        non_obs = []  # Store non-BPR imbalances

        for ob in self._orderblocks[timeframe]:
            if ob.name == "SCOB" or ob.name == "OB":
                candle_ids = frozenset(candle.id for candle in ob.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_ob.append(ob)
                    seen_candle_sets.add(candle_ids)  # Mark as seen
            else:
                non_obs.append(ob)  # Keep non-BPR imbalances

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._orderblocks[timeframe] = unique_ob + non_obs

    # region Duplicate Detection
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

    def _remove_duplicate_bpr(self, timeframe: int):
        if timeframe not in self._imbalances:
            return

        unique_bpr_candles = []
        seen_candle_sets = set()  # Track unique sets of candle IDs
        non_bpr_imbalances = []  # Store non-BPR imbalances

        for imbalance in self._imbalances[timeframe]:
            if imbalance.name == "BPR" or imbalance.name == "IFVG" or imbalance.name == "FVG":
                candle_ids = frozenset(candle.id for candle in imbalance.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_bpr_candles.append(imbalance)
                    seen_candle_sets.add(candle_ids)  # Mark as seen
            else:
                non_bpr_imbalances.append(imbalance)  # Keep non-BPR imbalances

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._imbalances[timeframe] = unique_bpr_candles + non_bpr_imbalances

    # endregion
