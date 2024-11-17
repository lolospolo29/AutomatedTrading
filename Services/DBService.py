from typing import Any


class DBService:
    def __init__(self, Mapper, mongoDBData, mongoDBTrades):
        self._Mapper = Mapper
        self._MongoDBData = mongoDBData
        self._MongoDBTrades = mongoDBTrades

    def autoMapper(self, data):
        return self._Mapper.MapToClass(data)

    def addDataToDB(self, collectionName: str, data: Any) -> None:
        self._MongoDBData.addDataToDB(collectionName, data)

    def addTradeToDB(self, trade: Any) -> bool:
        self._MongoDBTrades.add("OpenTrades", trade)
        return True

    def archiveCloseTrade(self, closedTradeList: list) -> None:
        self._MongoDBTrades.archiveCloseTrade(closedTradeList)

    def archiveData(self, assetName: str) -> Any:
        self._MongoDBData.archiveData(assetName)

    def receiveData(self,asset:str, broker:str, timeFrame:int,lookback: int):
        return self._MongoDBData.receiveData(asset, broker, timeFrame,lookback)

    def returnOpenTrades(self) -> list:
        return self._MongoDBTrades.returnOpenTrades()


