import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from app.models.asset.Asset import Asset
from app.models.asset.Candle import Candle


class AssetRepository:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AssetRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            self.__secret = self._secret_manager.return_secret("mongodb")
            self._dto_mapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    # Candle CRUD

    def add_candle(self, asset: str, candle: Candle):
        db = MongoDB(dbName="TradingData",uri= self.__secret)
        db.add(asset, candle.model_dump())

    # endregion

    # region Asset Class CRUD

    def find_asset_class_by_name(self,name:str)->AssetClassDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("name", name)

        return AssetClassDTO(**db.find("AssetClasses",query)[0])

    def find_asset_class_by_id(self,_id:int)->AssetClassDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("assetClassId", _id)
        return AssetClassDTO(**db.find("AssetClasses",query)[0])
    # endregion

    # region Asset CRUD

    def find_assets(self)->list[AssetDTO]:

        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        assets_db: list = db.find("Asset", None)

        assets:list[AssetDTO] = []

        for asset in assets_db:
            assets.append(AssetDTO(**asset))

        return assets

    def find_asset_by_id(self,asset_id:int)->AssetDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("assetId", asset_id)
        return AssetDTO(**db.find("Asset",query)[0])

    def add_asset(self,asset:Asset):
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        assetClass:AssetClassDTO = self.find_asset_class_by_name(asset.asset_class)

        assets_dtos:list[AssetDTO] = self.find_assets()

        highest_id = max(assets_dtos, key=lambda x: x.assetId).assetId

        dto:AssetDTO = self._dto_mapper.map_asset_to_dto(asset,assetClass.assetClassId,highest_id+1)

        db.add("Asset",dto.model_dump())

    def delete_asset(self,asset:Asset):
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        dto:AssetDTO = self.find_asset_by_id(asset.asset_id)

        db.delete("Asset",dto.id)

    def update_asset(self,asset:Asset):
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        assetClass:AssetClassDTO = self.find_asset_class_by_name(asset.asset_class)

        asset_dto = self.find_asset_by_id(asset.asset_id)

        dto = self._dto_mapper.map_asset_to_dto(asset=asset,asset_id=asset.asset_id,asset_class_id=assetClass.assetClassId)

        db.update("Asset",asset_dto.id,dto.model_dump())
    # endregion

    def find_smt_pair_by_id(self,strategyId:int=None,assetAId:int=None,assetBId:int=None)->list[SMTPairDTO]:
        if strategyId is None and assetAId is None and assetBId is None:
            return []
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        # Build the query dynamically, excluding None values
        query = {k: v for k, v in {
            "strategyId": strategyId,
            "assetAId": assetAId,
            "assetBId": assetBId
        }.items() if v is not None}

        smt_pairs: list[SMTPairDTO] = []
        smt_pairs_db: list = db.find("SMTPairs", query)

        for smt_pair in smt_pairs_db:
            smt_pairs.append(SMTPairDTO(**smt_pair))

        return smt_pairs
