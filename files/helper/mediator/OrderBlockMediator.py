import threading

from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.pdarray.orderblock.Breaker import Breaker
from files.models.frameworks.pdarray.orderblock.OrderBlock import Orderblock
from files.models.frameworks.pdarray.orderblock.OrderBlockStatusEnum import OrderBlockStatusEnum
from files.models.frameworks.pdarray.orderblock.PB import PB
from files.models.frameworks.pdarray.orderblock.RejectionBlock import RejectionBlock
from files.models.frameworks.pdarray.orderblock.SCOB import SCOB

class OrderBlockMediator:
    def __init__(self):
        self._lock = threading.Lock()
        self._orderblocks: dict[int, list[PDArray]] = {}
        self._probulsion_blocks: dict[str, list[PDArray]] = {}

    def analyze(self,first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe,atr:float):
        with self._lock:

            self._detect_orderblock(second_candle, third_candle, timeframe)
            self._detect_scob(first_candle, second_candle, third_candle, timeframe)
            self._detect_rejection_block(third_candle, timeframe,atr)
            self._detect_probulsion(third_candle, timeframe)

            self._detect_breaker(third_candle, timeframe)

            self._remove_duplicate_orderblocks(timeframe)

    def clear(self):
        self._orderblocks.clear()
        self._probulsion_blocks.clear()

    def get_orderblocks(self, timeframe: int) -> list[PDArray]:
        """Returns the orderblocks for a given timeframe."""
        return self._orderblocks.get(timeframe, [])

    def get_probulsion_blocks(self, timeframe: str) -> list[PDArray]:
        """Returns the propulsion blocks based on their ID."""
        return self._probulsion_blocks.get(timeframe, [])

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

    def _detect_rejection_block(self, third_candle: Candle, timeframe: int,atr:float):
        """Detects rejection patterns."""
        rejection_block = RejectionBlock.detect_rejection_block(candle=third_candle,
                                                                average_range=atr)

        if rejection_block:
            if timeframe not in self._orderblocks:
                self._orderblocks[timeframe] = []
            self._orderblocks[timeframe].append(rejection_block)

    def _detect_probulsion(self, third_candle: Candle, timeframe: int):
        """Detects probulsion patterns."""
        if timeframe in self._orderblocks:
            for orderblock in self._orderblocks[timeframe]:
                if orderblock.__name == "OB" or orderblock.__name == "SCOB":
                    pb = PB.detect_probulsion_block(last_candle=third_candle, orderblock=orderblock)
                    if pb:
                        pb.reference = orderblock.id
                        if timeframe not in self._probulsion_blocks:
                            self._probulsion_blocks[pb.reference] = []
                        self._probulsion_blocks[pb.reference].append(pb)

    def _detect_breaker(self, third_candle: Candle, timeframe: int):
        if timeframe in self._orderblocks:
            for orderblock in self._orderblocks[timeframe]:
                if orderblock.__name == "OB" or orderblock.__name == "SCOB":
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

    def _remove_duplicate_orderblocks(self, timeframe: int):
        if timeframe not in self._orderblocks:
            return

        unique_ob = []
        seen_candle_sets = set()  # Track unique sets of candle IDs
        non_obs = []  # Store non-BPR imbalances

        for ob in self._orderblocks[timeframe]:
            if ob.__name == "SCOB" or ob.__name == "OB":
                candle_ids = frozenset(candle.id for candle in ob.candles)  # Get unique candle IDs

                if candle_ids not in seen_candle_sets:
                    unique_ob.append(ob)
                    seen_candle_sets.add(candle_ids)  # Mark as seen
            else:
                non_obs.append(ob)  # Keep non-BPR imbalances

        # Combine filtered BPR imbalances with non-BPR imbalances
        self._orderblocks[timeframe] = unique_ob + non_obs

    def remove_orderblock_by_ids(self,_ids:list,timeframe: int):
        self._remove_orderblocks_by_ids(_ids=_ids,timeframe=timeframe)
        self._remove_probulsion_blocks_by_ids(_ids=_ids,timeframe=timeframe)

    def _remove_orderblocks_by_ids(self, _ids, timeframe):
        self._orderblocks[timeframe] = [orderblocks for orderblocks in self._orderblocks[timeframe]
                                 if all(candle.id in _ids for candle in orderblocks.candles)]

    def _remove_probulsion_blocks_by_ids(self, _ids, timeframe):
        self._probulsion_blocks[timeframe] = [pb for pb in self._probulsion_blocks[timeframe]
                                 if all(candle.id in _ids for candle in pb.candles)]