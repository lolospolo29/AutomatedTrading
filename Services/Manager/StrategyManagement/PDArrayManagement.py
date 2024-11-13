from Models.StrategyAnalyse.PDArray import PDArray


class PDArrayManagement:
    def __init__(self):
        self.pdArray: list[PDArray] = []

    def addPDArray(self, pdArray: PDArray):
        for pd in self.pdArray:
            if self.comparePDArrays(pdArray, pd):
                for id in pdArray.Ids:
                    if pd.isIdPresent(id):
                        break
            self.pdArray.append(pdArray)

    def returnPDArrays(self, assetBrokerStrategyRelation, AssetBrokerStrategyRelation):
        arrayList = []
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                arrayList.append(pd)

    def removePDArray(self, _ids, assetBrokerStrategyRelation, AssetBrokerStrategyRelation):
        for pd in self.pdArray:
            if pd.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                for id in _ids:
                    if pd.isIdPresent(id):
                        self.pdArray.remove(pd)

    @staticmethod
    def comparePDArrays(pdArray1: PDArray, pdArray2: PDArray) ->bool:
        if (pdArray1.assetBrokerStrategyRelation.compare(pdArray2.assetBrokerStrategyRelation) and
                pdArray1.name == pdArray2.name and pdArray1.direction == pdArray2.direction):
            return True
        return False
