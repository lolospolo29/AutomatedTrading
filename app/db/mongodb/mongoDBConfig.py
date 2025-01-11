import threading
from typing import Any

from app.db.mongodb.MongoDB import MongoDB
from app.manager.initializer.SecretsManager import SecretsManager


class mongoDBConfig:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(mongoDBConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._SecretManager: SecretsManager = SecretsManager()
            self._MongoDBConfig: MongoDB = MongoDB("TradingConfig", self._SecretManager.returnSecret("mongodb"))
            self._initialized = True  # Markiere als initialisiert


    def loadData(self, collectionName: str, query: Any):
        return self._MongoDBConfig.find(collectionName,query)

    def findById(self,typ: str, attribute: str, id: int, getAttribute: str) -> str:
            query = self._MongoDBConfig.buildQuery(typ, attribute, id)
            assetDict = self.loadData(typ,query)
            for doc in assetDict:
                return (doc.get(typ)).get(getAttribute)
