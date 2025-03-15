from datetime import datetime, timedelta

from files.db.mongodb.MongoDB import MongoDB
from files.mappers.DTOMapper import DTOMapper
from files.models.asset.Candle import Candle


class DataRepository:

    def __init__(self, db_name:str,uri:str,dto_mapper:DTOMapper):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = dto_mapper

    # Candle CRUD

    def fetch_candles_by_asset_and_timeframe(self, asset: str, timeframe: int, lookback_candles: int):
        """
        Ruft Candles aus MongoDB anhand des Assets, Timeframes und der Lookback-Periode ab.

        :param asset:
        :param timeframe: Timeframe in Minuten (z. B. 1, 5, 60, 1440)
        :param lookback_candles: Anzahl der vergangenen Candles (z. B. 100 letzte Candles)
        :return: Liste von Candle-Objekten
        """

        # Aktuelle UTC-Zeit
        end_date = datetime.utcnow()

        # Berechne den Startzeitpunkt: timeframe * lookback_candles
        minutes_to_subtract = timeframe * lookback_candles
        start_date = end_date - timedelta(minutes=minutes_to_subtract)

        # MongoDB-Query aufbauen
        query = {
            "asset": asset,
            "timeframe": timeframe,  # Timeframe ist bereits in Minuten gespeichert
            "iso_time": {"$gte": start_date, "$lte": end_date}
        }

        # Daten abrufen
        candles_db = self._db.find(collectionName=asset,query=query) # Neueste zuerst

        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles

    def add_candle(self, asset: str, candle: Candle):
        self._db.add(asset, candle.model_dump())

    def find_candles_by_asset(self, asset:str)->list[Candle]:
        query = self._db.buildQuery("asset", asset)

        candles_db:list = self._db.find(collectionName=asset,query=query)
        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles