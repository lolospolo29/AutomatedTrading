import datetime
import threading
from typing import Any

import pytz

from app.db.mongodb.MongoDB import MongoDB
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.TradeMapper import TradeMapper
from app.models.asset.Candle import Candle
from app.monitoring.logging.logging_startup import logger

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
            self._trade_mapper:TradeMapper = TradeMapper()
            self._mongo_db_data: MongoDB = MongoDB("TradingData", self._secret_manager.return_secret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    def add_candle_to_db(self, asset: str, candle: Candle):
        self._mongo_db_data.add(asset, candle.to_dict())

    def archive_data(self, asset: str) -> Any:
        logger.info(f"Arching data for {asset}")
        current_time_ny = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        date60_days_ago_ny = current_time_ny - datetime.timedelta(days=60)

        # Umwandlung beider Zeiten in UTC
        date60_days_ago_utc = date60_days_ago_ny.astimezone(pytz.utc)

        query = 'AssetData.timeStamp'

        self._mongo_db_data.deleteOldDocuments(asset, query, date60_days_ago_utc)

    def receive_data(self, asset: str, broker: str, timeframe: int, lookback: int):
        logger.info("Receiving Data from MongoDB")
        current_time_ny = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        three_days_ago = current_time_ny - datetime.timedelta(days=lookback)

        three_days_ago_utc = three_days_ago.astimezone(pytz.utc)

        query = {
            "Candle.broker": broker,
            "Candle.timeFrame": timeframe,
            "Candle.iso_time": {"$gte": three_days_ago_utc}
        }
        return self._mongo_db_data.find(asset, query)

    def receive_asset_data(self,asset)->list[Candle]:
        candlesDict:list =  self._mongo_db_data.find(asset, None)
        candles:list[Candle] = []
        for candle in candlesDict:
            try:
                candles.append(self._trade_mapper.map_candle(candle))
            finally:
                continue

        return candles
