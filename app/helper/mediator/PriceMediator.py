import threading

from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.frameworks.level.ADR import ADR
from app.models.frameworks.pdarray.Swing import Swing
from app.models.frameworks.pdarray.opens.NDOG import NDOG
from app.models.frameworks.pdarray.opens.NWOG import NWOG
from app.models.frameworks.pdarray.orderblock.OrderBlock import Orderblock
from app.models.frameworks.pdarray.orderblock.SCOB import SCOB

class PriceMediator:
    def __init__(self):
        self._lock = threading.Lock()
        self.candles:dict[int,list[Candle]] = {}
        self.swings:dict[int,list[PDArray]] = {}
        self.orderblocks:dict[int,list[PDArray]] = {}
        self.ndog:list[PDArray] = []
        self.nwog:list[PDArray] = []
        self.adr:float = 0.0

    def _calculate_average_range(self,timeframe:int):
        candles = self.candles[timeframe]
        high = max(candle.high for candle in candles)
        low = min(candle.low for candle in candles)
        self.adr = ADR.calculate_adr(high, low)

    def get_current_adr(self,timeframe)->float:
        self._calculate_average_range(timeframe)
        return self.adr

    def addCandle(self, candle:Candle):
        with self._lock:
            if candle.timeframe not in self.candles:
                self.candles[candle.timeframe] = []
            self.candles[candle.timeframe].append(candle)

    def detect_pd_arrays(self,timeframe:int):
        with self._lock:

            first_candle, second_candle, third_candle =  self.candles[timeframe][-3:]

            if NDOG.is_ndog(first_candle=second_candle, second_candle=third_candle):
                self.ndog.append(third_candle)

            if NWOG.is_nwog(first_candle=second_candle, second_candle=third_candle):
                self.nwog.append(third_candle)

            swing = Swing.detect_swing(first_candle, second_candle, third_candle)
            if swing:
                if timeframe not in self.swings:
                    self.swings[timeframe] = []
                self.swings[timeframe].append(swing)

            orderblock = Orderblock.return_pd_arrays(first_candle=second_candle, second_candle=third_candle)
            if orderblock:
                if timeframe not in self.orderblocks:
                    self.orderblocks[timeframe] = []
                self.orderblocks[timeframe].append(orderblock)

            scob = SCOB.detect_pd_single_candle_ob(first_candle, second_candle, third_candle)
            if scob:
                if timeframe not in self.orderblocks:
                    self.orderblocks[timeframe] = []
                self.orderblocks[timeframe].append(scob)