from Core.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Core.Main.Asset.Candle import Candle
from Core.Pattern.Mediator.PDMediator import PDMediator
from Core.StrategyAnalyse.PDArray import PDArray


class PDArrayHandler:
    def __init__(self):
        self.pdArray: list[PDArray] = []
        self._PDMediator: PDMediator = PDMediator()

    def addPDArray(self, pdArray: PDArray):
        for pd in self.pdArray:
            if self.comparePDArrays(pdArray, pd):
                return False
        self.pdArray.append(pdArray)

    def addCandleToPDArrayByIds(self, candles: list[Candle],timeFrame: int,
                                assetBrokerStrategyRelation: AssetBrokerStrategyRelation):
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

    def returnPDArrays(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        arrayList = []
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                arrayList.append(pd)
        return arrayList

    def removePDArray(self, _ids: list, assetBrokerStrategyRelation: AssetBrokerStrategyRelation,
                      timeFrame: int) -> None:
        pdArrays = self.pdArray.copy()
        for pd in pdArrays:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and pd.timeFrame == timeFrame:
                if not pd.isIdPresent(_ids):
                    self.pdArray.remove(pd)

    @staticmethod
    def comparePDArrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        if (pdArray1.assetBrokerStrategyRelation.compare(pdArray2.assetBrokerStrategyRelation) and
                pdArray1.name == pdArray2.name and sorted(pdArray1.Ids) == sorted(pdArray2.Ids)
                and pdArray1.direction == pdArray2.direction):
            return True
        return False
