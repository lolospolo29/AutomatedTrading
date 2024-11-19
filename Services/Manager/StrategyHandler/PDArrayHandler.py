from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.StrategyAnalyse.PDArray import PDArray


class PDArrayHandler:
    def __init__(self):
        self.pdArray: list[PDArray] = []

    def addPDArray(self, pdArray: PDArray):
        for pd in self.pdArray:
            if self.comparePDArrays(pdArray, pd):
                return False
        self.pdArray.append(pdArray)

    def returnPDArrays(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        arrayList = []
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                arrayList.append(pd)
        return arrayList

    def removePDArray(self, _ids: list, assetBrokerStrategyRelation: AssetBrokerStrategyRelation,
                      timeFrame: int) -> None:
        for pd in self.pdArray:
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
