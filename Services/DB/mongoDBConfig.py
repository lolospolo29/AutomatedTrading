from typing import Any

from Core.DB.MongoDB import MongoDB
from Services.Helper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager


class mongoDBConfig:
    def __init__(self, secretsManager: SecretsManager, DataMapper: Mapper):
        self._SecretManager: SecretsManager = secretsManager
        self._DataMapper: Mapper = DataMapper
        self._MongoDBConfig: MongoDB = MongoDB("TradingConfig", self._SecretManager.returnSecret("mongodb"))

    def loadData(self, collectionName: str, query: Any):
        return self._MongoDBConfig.find(collectionName,query)

    def findById(self,typ: str, attribute: str, id: int, getAttribute: str) -> str:
            query = self._MongoDBConfig.buildQuery(typ, attribute, id)
            assetDict = self.loadData(typ,query)
            for doc in assetDict:
                return (doc.get(typ)).get(getAttribute)
