import threading
import time

from app.db.modules.MongoDB import MongoDB
from app.db.modules.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.SecretsManager import SecretsManager
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.frameworks.PDArray import PDArray
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade


class mongoDBTrades:
    # region Initializing
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
    # endregion

    def addTradeToDB(self, trade: Trade):
        self._MongoDBTrades.add(MongoEndPointEnum.OPENTRADES.value, trade.toDict())

    def updateTrade(self, trade: Trade):
        query = self._MongoDBTrades.buildQuery("Trade","id", str(trade.id))
        res = self._MongoDBTrades.find(MongoEndPointEnum.OPENTRADES.value, query)
        self._MongoDBTrades.update(MongoEndPointEnum.OPENTRADES.value, res[0].get("_id"), trade.toDict())

    def archiveTrade(self, trade: Trade):
        self._MongoDBTrades.add(MongoEndPointEnum.CLOSEDTRADES.value, trade.toDict())
        query = self._MongoDBTrades.buildQuery("Trade", "id", str(trade.id))
        self._MongoDBTrades.deleteByQuery(MongoEndPointEnum.OPENTRADES.value, query)

    def addOrderToDB(self, order: Order):
        self._MongoDBTrades.add(MongoEndPointEnum.OPENORDERS.value, order.toDict())

    def updateOrder(self, order: Order):
        query = self._MongoDBTrades.buildQuery("Order","orderLinkId", str(order.orderLinkId))
        res = self._MongoDBTrades.find(MongoEndPointEnum.OPENORDERS.value, query)
        self._MongoDBTrades.update(MongoEndPointEnum.OPENORDERS.value, res[0].get("_id"), order.toDict())

    def archiveOrder(self, order: Order):
        self._MongoDBTrades.add(MongoEndPointEnum.CLOSEDORDERS.value, order.toDict())
        query = self._MongoDBTrades.buildQuery("Order","orderLinkId", str(order.orderLinkId))
        self._MongoDBTrades.deleteByQuery(MongoEndPointEnum.OPENORDERS.value, query)
