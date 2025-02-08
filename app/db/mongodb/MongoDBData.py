import datetime
import threading
from typing import Any

import pytz

from app.db.mongodb.MongoDB import MongoDB
from app.manager.initializer.SecretsManager import SecretsManager
from app.models.asset.Candle import Candle
from app.monitoring.logging.logging_startup import logger



class MongoDBData(MongoDB):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MongoDBData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            self._dto_mapper = None
            super().__init__("TradingData", self._secret_manager.return_secret("mongodb"))
            self.tz =  pytz.timezone('America/New_York')
            self._initialized = True  # Markiere als initialisiert

    def add_candle_to_db(self, asset: str, candle: Candle):
        self.add(asset, candle.model_dump_json())

    def archive_data(self, asset: str) -> Any:
        logger.info(f"Arching data for {asset}")
        current_time_ny = datetime.datetime.now(self.tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        date60_days_ago_ny = current_time_ny - datetime.timedelta(days=60)

        # Umwandlung beider Zeiten in UTC
        date60_days_ago_utc = date60_days_ago_ny.astimezone(pytz.utc)

        self.deleteOldDocuments(asset, "timestamp", date60_days_ago_utc)

    def receive_data(self, asset: str, broker: str, timeframe: int, lookback: int):
        logger.info("Receiving Data from MongoDB")
        current_time_ny = datetime.datetime.now(self.tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        three_days_ago = current_time_ny - datetime.timedelta(days=lookback)

        three_days_ago_utc = three_days_ago.astimezone(pytz.utc)

        query = {
            "broker": broker,
            "timeFrame": timeframe,
            "iso_time": {"$gte": three_days_ago_utc}
        }
        return self.find(asset, query)

    def receive_asset_data(self, asset) -> list:
        return self.find(asset, None)

