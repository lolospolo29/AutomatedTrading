import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper


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

    def find_relations_by_asset_id(self,asset_id:int)->list[RelationDTO]:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("assetId", asset_id)

        relations_db:list = db.find("Relation",query)

        relations:list[RelationDTO] = []

        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_broker_by_id(self,_id:int)->BrokerDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("brokerId", _id)
        return BrokerDTO(**db.find("Broker",query)[0])

    def find_strategy_by_id(self,_id:int)->StrategyDTO:
        db = MongoDB(dbName="TradingConfig",uri=self.__secret)

        query = db.buildQuery("strategyId", _id)
        return StrategyDTO(**db.find("Strategy",query)[0])