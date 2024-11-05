from Models.DB.MongoDB import MongoDB
from Services.Helper.Mapper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager


class mongoDBConfig:
    def __init__(self, secretsManager: SecretsManager, DataMapper: Mapper):
        self._SecretManager: SecretsManager = secretsManager
        self._DataMapper: Mapper = DataMapper
        self._MongoDBConfig: MongoDB = MongoDB("TradingConfig", self._SecretManager.returnSecret("mongodb"))

    def loadData(self, collectionName: str):
        return self._MongoDBConfig.find(collectionName,None)
