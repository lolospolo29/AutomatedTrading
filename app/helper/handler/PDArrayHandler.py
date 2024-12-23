import threading

from app.helper.mediator.PDMediator import PDMediator
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class PDArrayHandler:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(PDArrayHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self.pdArray: list[PDArray] = []
            self._PDMediator: PDMediator = PDMediator()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Add / Return Functions
    def addPDArray(self, pdArray: PDArray)->bool:
        for pd in self.pdArray:
            if self._comparePDArrays(pdArray, pd):
                return False
        self.pdArray.append(pdArray)
        return True

    def addCandleToPDArrayByIds(self, candles: list[Candle],timeFrame: int,
                                assetBrokerStrategyRelation: AssetBrokerStrategyRelation)-> None:
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and pd.timeFrame == timeFrame:

                existing_ids = {candle.id for candle in pd.candles}  # Cache existing IDs
                new_candles = [
                    candle for candle in candles
                    if candle.id in pd.Ids and candle.id not in existing_ids
                ]

                # Assuming pd.addCandles accepts a list of candles
                if new_candles:
                    pd.addCandles(new_candles)


    def returnPDArrays(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        arrayList = []
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                arrayList.append(pd)
        return arrayList
    # endregion

    # region Remove / Compare / Update
    def removePDArray(self, _ids: list, assetBrokerStrategyRelation: AssetBrokerStrategyRelation,
                      timeFrame: int) -> None:
        pdArrays = self.pdArray.copy()
        for pd in pdArrays:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and pd.timeFrame == timeFrame:
                if not pd.isIdPresent(_ids):
                    self.pdArray.remove(pd)

    def updatePDArrays(self, candles: list[Candle],timeFrame: int,
                                assetBrokerStrategyRelation: AssetBrokerStrategyRelation):
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and pd.timeFrame == timeFrame:

                direction = self._PDMediator.checkForInverse(pd.name,pd,candles)
                if direction != pd.direction:
                        pd.status = "Inversed"
                        continue

                if direction == pd.direction:
                        pd.status = "Normal"
                        continue

    @staticmethod
    def _comparePDArrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        if (pdArray1.assetBrokerStrategyRelation.compare(pdArray2.assetBrokerStrategyRelation) and
                pdArray1.name == pdArray2.name and sorted(pdArray1.Ids) == sorted(pdArray2.Ids)
                and pdArray1.direction == pdArray2.direction):
            return True
        return False
    # endregion
