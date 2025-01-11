import datetime
import threading
from typing import Any

import pytz

from app.db.mongodb.MongoDB import MongoDB
from app.manager.initializer.SecretsManager import SecretsManager
from app.models.asset.Candle import Candle

ny_tz = pytz.timezone('America/New_York')


class mongoDBData:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(mongoDBData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._SecretManager: SecretsManager = SecretsManager()
            self._MongoDBData: MongoDB = MongoDB("TradingData", self._SecretManager.returnSecret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    def addCandleToDB(self, asset:str,candle: Candle):
        self._MongoDBData.add(asset, candle)

    def archiveData(self, asset: str) -> Any:
        currentTimeNy = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        date60DaysAgoNy = currentTimeNy - datetime.timedelta(days=60)

        # Umwandlung beider Zeiten in UTC
        currentTimeUtc = currentTimeNy.astimezone(pytz.utc)
        date60DaysAgoUtc = date60DaysAgoNy.astimezone(pytz.utc)

        query = 'AssetData.timeStamp'

        self._MongoDBData.deleteOldDocuments(asset, query, date60DaysAgoUtc)

    def receiveData(self,asset:str, broker:str, timeFrame:int, lookback: int):
        currentTimeNy = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        three_days_ago = currentTimeNy - datetime.timedelta(days=lookback)

        three_days_ago_utc = three_days_ago.astimezone(pytz.utc)

        query = {
            "Candle.broker": broker,
            "Candle.timeFrame": timeFrame,
            "Candle.IsoTime": {"$gte": three_days_ago_utc}
        }
        return self._MongoDBData.find(asset, query)