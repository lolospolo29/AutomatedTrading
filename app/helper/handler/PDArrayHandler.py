import threading

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray


class PDArrayHandler:


    def __init__(self):
        self.pdArray: list[PDArray] = []
        _lock = threading.Lock()

    def addPDArray(self, pdArray: PDArray)->bool:
        for pd in self.pdArray:
            if self._comparePDArrays(pdArray, pd):
                return False
        self.pdArray.append(pdArray)
        return True

    def returnPDArrays(self) -> list[PDArray]:
        return self.pdArray

    def removePDArray(self, candles: list[Candle],timeFrame: int) -> None:
        _ids = [candle.id for candle in candles]
        pdArrays = self.pdArray.copy()
        for pd in pdArrays:
            if pd.timeFrame == timeFrame:
                if not pd.isIdPresent(_ids):
                    self.pdArray.remove(pd)

    @staticmethod
    def _comparePDArrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        _1ids = [candle.id for candle in pdArray1.candles]
        _2ids = [candle.id for candle in pdArray2.candles]
        if (pdArray1.name == pdArray2.name and sorted(_1ids) == sorted(_2ids) and
                pdArray1.direction == pdArray2.direction):
            return True
        return False
