import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from app.models.asset.Relation import Relation


class RelationRepository:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RelationRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            self.__secret = self._secret_manager.return_secret("mongodb")
            self._dto_mapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    def add_relation(self,relation:Relation):
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        asset_dto:AssetDTO = self.find_asset_by_name(relation.asset)
        broker_dto:BrokerDTO = self.find_broker_by_name(relation.broker)
        strategy_dto:StrategyDTO = self.find_strategy_by_name(relation.strategy)

        relations_dtos:list[RelationDTO] = self.find_relations()

        highest_id = max(relations_dtos, key=lambda x: x.relationId).relationId

        relation_dto = RelationDTO(assetId=asset_dto.assetId,brokerId=broker_dto.brokerId
                                   ,strategyId=strategy_dto.strategyId
                                   ,maxTrades=relation.max_trades,relationId=highest_id+1)

        db.add("Relation",relation_dto.model_dump())

    def find_relations(self):
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        relations_db:list = db.find("Relation",None)
        relations:list[RelationDTO] = []
        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_relations_by_asset_id(self,asset_id:int)->list[RelationDTO]:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("assetId", asset_id)

        relations_db:list = db.find("Relation",query)

        relations:list[RelationDTO] = []

        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_asset_by_name(self,name:str)->AssetDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("name", name)
        return AssetDTO(**db.find("Asset",query)[0])

    def find_broker_by_name(self,name:str)->BrokerDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("name", name)
        return BrokerDTO(**db.find("Broker",query)[0])

    def find_strategy_by_name(self,name:str)->StrategyDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("name", name)
        return StrategyDTO(**db.find("Strategy",query)[0])

    def find_broker_by_id(self,_id:int)->BrokerDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("brokerId", _id)
        return BrokerDTO(**db.find("Broker",query)[0])

    def find_strategy_by_id(self,_id:int)->StrategyDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("strategyId", _id)
        return StrategyDTO(**db.find("Strategy",query)[0])