from files.db.mongodb.MongoDB import MongoDB
from files.mappers.DTOMapper import DTOMapper
from files.models.asset.Candle import Candle


class DataRepository:

    def __init__(self, db_name:str,uri:str):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = DTOMapper()

    # Candle CRUD

    def add_candle(self, asset: str, candle: Candle):
        self._db.add(asset, candle.model_dump())

    def find_candles_by_asset(self, asset:str)->list[Candle]:
        query = self._db.buildQuery("asset", asset)

        candles_db:list = self._db.find(collectionName=asset,query=query)
        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles