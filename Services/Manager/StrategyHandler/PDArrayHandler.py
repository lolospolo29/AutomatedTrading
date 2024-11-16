from numpy import sort

from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.StrategyAnalyse.PDArray import PDArray


class PDArrayHandler:
    def __init__(self):
        self.pdArray: list[PDArray] = []

    def addPDArray(self, pdArray: PDArray):
        for pd in self.pdArray:
            if self.comparePDArrays(pdArray, pd):
                break
            self.pdArray.append(pdArray)

    def returnPDArrays(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        arrayList = []
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                arrayList.append(pd)
        return arrayList

    def removePDArray(self, _ids, assetBrokerStrategyRelation: AssetBrokerStrategyRelation):
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                for id in _ids:
                    if pd.isIdPresent(id):
                        self.pdArray.remove(pd)
                        continue

    @staticmethod
    def comparePDArrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        if (pdArray1.assetBrokerStrategyRelation.compare(pdArray2.assetBrokerStrategyRelation) and
                pdArray1.name == pdArray2.name and sort(pdArray1.Ids) == sort(pdArray2.Ids)
                and pdArray1.direction == pdArray2.direction):
            return True
        return False
