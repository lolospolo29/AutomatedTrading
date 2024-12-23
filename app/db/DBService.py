import threading
from typing import Any

from app.db.modules.mongoDBData import mongoDBData
from app.db.modules.mongoDBTrades import mongoDBTrades


class DBService:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DBService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._MongoDBData = mongoDBData()
            self._MongoDBTrades = mongoDBTrades()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region db Data Functions
    def addDataToDB(self, collectionName: str, data: Any) -> None:
        self._MongoDBData.addDataToDB(collectionName, data)

    def receiveData(self,asset:str, broker:str, timeFrame:int,lookback: int):
        return self._MongoDBData.receiveData(asset, broker, timeFrame,lookback)

    def archiveData(self, assetName: str) -> Any:
        self._MongoDBData.archiveData(assetName)
    # endregion

    # region db Trade Functions

    def addTradeToDB(self, trade: Any) -> bool:
        self._MongoDBTrades.add("OpenTrades", trade)
        return True

    def archiveCloseTrade(self, closedTradeList: list) -> None:
        self._MongoDBTrades.archiveCloseTrade(closedTradeList)

    def returnOpenTrades(self) -> list:
        return self._MongoDBTrades.returnOpenTrades()

    # endregion
