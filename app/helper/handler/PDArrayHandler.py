import threading

from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.monitoring.logging.logging_startup import logger


class PDArrayHandler:


    def __init__(self):
        self.pdArray: list[PDArray] = []
        self._lock = threading.Lock()

    def add_pd_array(self, pdArray: PDArray)->bool:
        with self._lock:
            try:
                for pd in self.pdArray:
                    if self._compare_pd_arrays(pdArray, pd):
                        return False
                self.pdArray.append(pdArray)
                return True
            except Exception as e:
                logger.error("Add PD Array Exception: {}".format(e))

    def return_pd_arrays(self) -> list[PDArray]:
        with self._lock:
            return self.pdArray

    def remove_pd_array(self, candles: list[Candle], timeframe: int) -> None:
        with self._lock:
            try:
                _ids = [candle.id for candle in candles]
                pdArrays = self.pdArray.copy()
                for pd in pdArrays:
                    pd:PDArray = pd
                    if pd.timeframe == timeframe:
                        ids  = [candle.id for candle in pd.candles]
                        if not all(id in _ids for id in ids):  # Ensures every `id` in `ids` exists in `_ids`
                            self.pdArray.remove(pd)
            except Exception as e:
                logger.error("Remove PD Array Exception: {}".format(e))

    @staticmethod
    def _compare_pd_arrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        _1ids = [candle.id for candle in pdArray1.candles]
        _2ids = [candle.id for candle in pdArray2.candles]
        if (pdArray1.name == pdArray2.name and sorted(_1ids) == sorted(_2ids) and
                pdArray1.direction == pdArray2.direction):
            return True
        return False
