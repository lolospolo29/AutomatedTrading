import threading
from typing import Any

from app.db.modules.MongoDB import MongoDB
from app.manager.SecretsManager import SecretsManager
from app.models.trade.Trade import Trade


class mongoDBTrades:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(mongoDBTrades, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._SecretManager: SecretsManager = SecretsManager()
            self._MongoDBTrades: MongoDB = MongoDB("Trades", self._SecretManager.returnSecret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    def addTradeToDB(self, trade: Any) -> bool:
        self._MongoDBTrades.add("OpenTrades", trade)
        return True
