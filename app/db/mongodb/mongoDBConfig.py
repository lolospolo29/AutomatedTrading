import threading
from typing import Any

from app.db.mongodb.MongoDB import MongoDB
from app.manager.initializer.SecretsManager import SecretsManager
from app.monitoring.logging.logging_startup import logger


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

            self._secret_manager: SecretsManager = SecretsManager()
            self._mongo_db_config: MongoDB = MongoDB("TradingConfig", self._secret_manager.return_secret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    def load_data(self, collectionName: str, query: Any):
        return self._mongo_db_config.find(collectionName, query)

    def find_by_id(self, typ: str, attribute: str, id: int, getAttribute: str) -> str:
        logger.info("Finding {typ} by id {id}".format(typ=typ, id=id))
        query = self._mongo_db_config.buildQuery(typ, attribute, id)
        asset_dict = self.load_data(typ, query)
        for doc in asset_dict:
            return (doc.get(typ)).get(getAttribute)
# todo requestdb class foreach db
# todo logging status for how far trade,order,setup is in process