import threading

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray


class PDArrayHandler:


    def __init__(self):
        self.pdArray: list[PDArray] = []
        _lock = threading.Lock()

    def add_pd_array(self, pdArray: PDArray)->bool:
        for pd in self.pdArray:
            if self._compare_pd_arrays(pdArray, pd):
                return False
        self.pdArray.append(pdArray)
        return True

    def return_pd_arrays(self) -> list[PDArray]:
        return self.pdArray

    def remove_pd_array(self, candles: list[Candle], timeFrame: int) -> None:
        _ids = [candle.id for candle in candles]
        pdArrays = self.pdArray.copy()
        for pd in pdArrays:
            if pd.timeframe == timeFrame:
                if not pd.is_id_present(_ids):
                    self.pdArray.remove(pd)

    @staticmethod
    def _compare_pd_arrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        _1ids = [candle.id for candle in pdArray1.candles]
        _2ids = [candle.id for candle in pdArray2.candles]
        if (pdArray1.name == pdArray2.name and sorted(_1ids) == sorted(_2ids) and
                pdArray1.direction == pdArray2.direction):
            return True
        return False
