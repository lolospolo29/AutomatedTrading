from datetime import datetime, timedelta

from files.db.MongoDB import MongoDB
from files.models.asset.Candle import Candle


class CandleRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Candle

    def add_candle(self, asset: str, candle: Candle):
        self._db.add(asset, candle.model_dump(exclude={"_id"}))

    def find_candles_by_asset(self, asset:str)->list[Candle]:
        query = self._db.build_query("asset", asset)

        candles_db:list = self._db.find(collection_name=asset, query=query)
        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles

    def find_candles_with_lookback(self, asset: str, timeframe: int, lookback_candles: int)->list[Candle]:
        end_date = datetime.utcnow()

        minutes_to_subtract = timeframe * lookback_candles
        start_date = end_date - timedelta(minutes=minutes_to_subtract)

        query = {
            "asset": asset,
            "timeframe": timeframe,
            "iso_time": {"$gte": start_date, "$lte": end_date}
        }

        candles_db = self._db.find(collection_name=asset, query=query)

        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles

    # endregion