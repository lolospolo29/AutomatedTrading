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

            self._secret_manager: SecretsManager = SecretsManager()
            self._mongo_db_data: MongoDB = MongoDB("TradingData", self._secret_manager.return_secret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    def add_candle_to_db(self, asset:str, candle: Candle):
        self._mongo_db_data.add(asset, candle)

    def archive_data(self, asset: str) -> Any:
        current_time_ny = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        date60_days_ago_ny = current_time_ny - datetime.timedelta(days=60)

        # Umwandlung beider Zeiten in UTC
        currentTimeUtc = current_time_ny.astimezone(pytz.utc)
        date60_days_ago_utc = date60_days_ago_ny.astimezone(pytz.utc)

        query = 'AssetData.timeStamp'

        self._mongo_db_data.deleteOldDocuments(asset, query, date60_days_ago_utc)

    def receive_data(self, asset:str, broker:str, timeframe:int, lookback: int):
        current_time_ny = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        three_days_ago = current_time_ny - datetime.timedelta(days=lookback)

        three_days_ago_utc = three_days_ago.astimezone(pytz.utc)

        query = {
            "Candle.broker": broker,
            "Candle.timeFrame": timeframe,
            "Candle.IsoTime": {"$gte": three_days_ago_utc}
        }
        return self._mongo_db_data.find(asset, query)