import threading

from files.helper.mediator.ImbalanceMediator import ImbalanceMediator
from files.helper.mediator.OrderBlockMediator import OrderBlockMediator
from files.helper.mediator.StructureMediator import StructureMediator
from files.helper.mediator.TImeMediator import TimeMediator
from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from files.models.frameworks.level.ADR import ADR
from files.models.frameworks.level.Fibonnaci import Fibonnaci

class PriceMediator:
    def __init__(self):
        self._lock = threading.Lock()

        self._ote = Fibonnaci([0.62, 0.705, 1.5], "OTE")
        self._pd = Fibonnaci([0.0, 0.5, 1.0], "PD")
        self._deviation = Fibonnaci([1.5, 2.0, 3.0, 4.0], "STDV")

        self._structure_mediator = StructureMediator()
        self._orderblock_mediator = OrderBlockMediator()
        self._imbalance_mediator = ImbalanceMediator()
        self._time_mediator = TimeMediator()

        self._ndog: list[PDArray] = []
        self._nwog: list[PDArray] = []
        self._pd_levels:list[Level] = []
        self._pw_levels:list[Level] = []
        self._pd_atr:float = 0.0
        self._today_atr: float = 0.0
        self._atr:dict[int,float] = {}

    def analyze(self, first_candle: Candle, second_candle: Candle, third_candle: Candle, timeframe):
        with self._lock:

            self._time_mediator.analyze(third_candle)

            self._calculate_average_range(first_candle, second_candle, third_candle, timeframe)

            self._orderblock_mediator.analyze(first_candle, second_candle, third_candle,timeframe,self._atr[timeframe])

            self._imbalance_mediator.analyze(first_candle, second_candle, third_candle,timeframe)

            self._structure_mediator.analyze(first_candle, second_candle, third_candle,timeframe,self._atr[timeframe])

    def add_ndog(self,candle: Candle):
        with self._lock:
            new_ndog = PDArray(candles=[candle],name="NDOG")
            for ndog in self._ndog:
                if candle in ndog:
                    return
            self._ndog.append(new_ndog)

    def add_nwog(self,candle: Candle):
        with self._lock:
            new_nwog = PDArray(candles=[candle],name="NWOG")
            for nwog in self._nwog:
                if candle in nwog:
                    return
            self._nwog.append(new_nwog)

    def add_previous_days_levels(self,candle: Candle):
        with self._lock:
            if candle.timeframe == 1440:
                new_pd_level = Level(candles=[candle], name="PreviousDay",level=0,fib_level=0)
                for pd in self._pd_levels:
                    if candle in pd:
                        return
                self._pd_levels.append(new_pd_level)

    def add_previous_week_level(self,candle: Candle):
        with self._lock:
            if candle.timeframe == 10080:
                pw_level = Level(candles=[candle], name="PreviousWeek",level=0,fib_level=0)
                for pw in self._pw_levels:
                    if candle in pw:
                        return
                self._pw_levels.append(pw_level)

    def set_today_atr(self,candle: Candle):
        with self._lock:
            self._today_atr = ADR.calculate_adr(candle.high,candle.low)

    def set_pd_atr(self,candle: Candle):
        with self._lock:
            self._pd_atr = ADR.calculate_adr(candle.high,candle.low)

    def get_ndogs(self) -> list[PDArray]:
        """Returns the NDOG patterns detected."""
        return self._ndog

    def get_nwogs(self) -> list[PDArray]:
        """Returns the NWOG patterns detected."""
        return self._nwog

    def get_atr(self, timeframe:int,previous:bool=False,today:bool=False) -> float:
        """Returns the current ADR (Average Daily Range)."""
        if previous:
            return self._pd_atr
        if today:
            return self._today_atr
        return self._atr[timeframe]

    def get_session_levels(self)->list[Level]:
        """Returns the current session levels."""
        return self._time_mediator.get_session_level()

    def get_order_blocks(self, timeframe: int) -> list[PDArray]:
        """Returns the current orderblock levels."""
        return self._orderblock_mediator.get_orderblocks(timeframe)

    def get_probulsion_block(self, orderblock_id: str) -> list[PDArray]:
        """Returns the current probulsion block."""
        return self._orderblock_mediator.get_probulsion_block(orderblock_id)

    def get_imbalance(self,timeframe:int) -> list[PDArray]:
        """Returns the current IMB (Average Daily Range)."""
        return self._imbalance_mediator.get_imbalances(timeframe)

    def get_eqhl(self, timeframe) -> list[Level]:
        return self._structure_mediator.get_eqhl(timeframe)

    def get_swings(self, timeframe) -> list[PDArray]:
        return self._structure_mediator.get_swings(timeframe)

    def get_structure(self, timeframe, previous:bool=False) -> list[Structure]:
        if previous:
            return self._structure_mediator.get_previous_structure(timeframe)
        return self._structure_mediator.get_current_structure(timeframe)

    def get_fibonnaci(self, candles: list[Candle], ote: bool = True, pd: bool = False, stdv: bool = False,
                      fib_levels: list[float] = None) -> list[Level]:
        highest_candle = max(candles, key=lambda candle: candle.high)
        lowest_candle = min(candles, key=lambda candle: candle.low)

        if fib_levels:
            return Fibonnaci(fib_levels, "User").return_levels(highest_candle, lowest_candle)
        if stdv:
            return self._deviation.return_levels(highest_candle, lowest_candle)
        if pd:
            return self._pd.return_levels(highest_candle, lowest_candle)
        if ote:
            return self._ote.return_levels(highest_candle, lowest_candle)

    def remove_old_frameworks(self, candles: list[Candle], timeframe):
        _ids = [candle.id for candle in candles]

        self._time_mediator.remove_old_sessions(_ids)
        self._imbalance_mediator.remove_imbalances_by_ids(_ids, timeframe)
        self._orderblock_mediator.remove_orderblock_by_ids(_ids, timeframe)
        self._structure_mediator.remove_by_ids(_ids, timeframe)

    def reset(self):
        with self._lock:
            self._imbalance_mediator.clear()
            self._orderblock_mediator.clear()
            self._structure_mediator.clear()
            self._time_mediator.clear()
            self._atr.clear()

    def _calculate_average_range(self, first_candle: Candle, second_candle: Candle, third_candle: Candle,
                                 timeframe: int):
        high = max(first_candle.high, second_candle.high, third_candle.high)
        low = min(first_candle.high, second_candle.high, third_candle.high)
        if self._atr == 0:
            self._atr[timeframe] = ADR.calculate_adr(high, low)
        else:
            self._atr[timeframe] = (self._atr[timeframe] + ADR.calculate_adr(high, low)) / 2