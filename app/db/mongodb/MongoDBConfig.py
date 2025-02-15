import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from app.models.asset.Asset import Asset


class MongoDBConfig(MongoDB):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MongoDBConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            super().__init__("TradingConfig", self._secret_manager.return_secret("mongodb"))
            self._dto_mapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    def find_assets(self)->list[AssetDTO]:

        assets_db: list = self.find("Asset", None)

        assets:list[AssetDTO] = []

        for asset in assets_db:
            assets.append(AssetDTO(**asset))

        return assets

    def add_asset(self,asset:Asset):

        assetClass:AssetClassDTO = self.find_asset_class_by_name(asset.asset_class)

        assets_dtos:list[AssetDTO] = self.find_assets()

        highest_id = max(assets_dtos, key=lambda x: x.assetId).assetId

        dto:AssetDTO = self._dto_mapper.map_asset_to_dto(asset,assetClass.assetClassId,highest_id+1)

        self.add("Asset",dto.model_dump())

    def delete_asset(self,asset:Asset):
        dto:AssetDTO = self.find_asset_by_name(asset.name)

        self.delete("Asset",dto.id)

    def update_asset(self,asset:Asset):
        dto:AssetDTO = self.find_asset_by_id(asset.asset_id)

        self.update("Asset",dto.id,dto.model_dump())

    def find_asset_by_id(self,asset_id:int)->AssetDTO:
        query = self.buildQuery("assetId", asset_id)
        return AssetDTO(**self.find("Asset",query)[0])

    def find_asset_by_name(self,name:str)->AssetDTO:
        query = self.buildQuery("name", name)
        return AssetDTO(**self.find("Asset",query)[0])

    def find_asset_class_by_name(self,name:str)->AssetClassDTO:
        query = self.buildQuery("name", name)
        return AssetClassDTO(**self.find("AssetClasses",query)[0])

    def find_relations_by_asset_id(self,asset_id:int)->list[RelationDTO]:
        query = self.buildQuery("assetId", asset_id)

        relations_db:list = self.find("Relation",query)

        relations:list[RelationDTO] = []

        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_asset_class_by_id(self,_id:int)->AssetClassDTO:
        query = self.buildQuery("assetClassId", _id)
        return AssetClassDTO(**self.find("AssetClasses",query)[0])

    def find_broker_by_id(self,_id:int)->BrokerDTO:
        query = self.buildQuery("brokerId", _id)
        return BrokerDTO(**self.find("Broker",query)[0])

    def find_strategy_by_id(self,_id:int)->StrategyDTO:
        query = self.buildQuery("strategyId", _id)
        return StrategyDTO(**self.find("Strategy",query)[0])

    def find_smt_pair_by_id(self,strategyId:int=None,assetAId:int=None,assetBId:int=None)->list[SMTPairDTO]:
        if strategyId is None and assetAId is None and assetBId is None:
            return []

        # Build the query dynamically, excluding None values
        query = {k: v for k, v in {
            "strategyId": strategyId,
            "assetAId": assetAId,
            "assetBId": assetBId
        }.items() if v is not None}

        smt_pairs: list[SMTPairDTO] = []
        smt_pairs_db: list = self.find("SMTPairs", query)

        for smt_pair in smt_pairs_db:
            smt_pairs.append(SMTPairDTO(**smt_pair))

        return smt_pairs


