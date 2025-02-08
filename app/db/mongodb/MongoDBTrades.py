import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.initializer.SecretsManager import SecretsManager
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class MongoDBTrades(MongoDB):
    # region Initializing
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MongoDBTrades, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            super().__init__("Trades", self._secret_manager.return_secret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def find_trade_or_trades_by_id(self, id: str = None):
        return self.find(MongoEndPointEnum.OPENTRADES.value, self.buildQuery("id", id))


    def find_order_or_orders_by_id(self, id: str = None) -> list[Order]:
        pass

    # region Add / Update / Archive
    def add_trade_to_db(self, trade: Trade):
        logger.info(f"Adding Trade to DB: {trade.id}")
        self.add(MongoEndPointEnum.OPENTRADES.value, trade.to_dict())

    def update_trade(self, trade: Trade):
        logger.info(f"Updating Trade,OrderLinkId:{trade.id}")
        query = self.buildQuery( "id", str(trade.id))
        res = self.find(MongoEndPointEnum.OPENTRADES.value, query)
        self.update(MongoEndPointEnum.OPENTRADES.value, res[0].get("_id"), trade.to_dict())

    def archive_trade(self, trade: Trade):
        logger.info(f"Arching Trade,OrderLinkId:{trade.id}")
        self.add(MongoEndPointEnum.CLOSEDTRADES.value, trade.to_dict())
        query = self.buildQuery( "id", str(trade.id))
        self.deleteByQuery(MongoEndPointEnum.OPENTRADES.value, query)

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")
        self.add(MongoEndPointEnum.OPENORDERS.value, order.to_dict())

    def update_order(self, order: Order):
        logger.info(f"Update Order To DB,OrderLinkId: {order.orderLinkId},Symbol: {order.symbol}")

        query = self.buildQuery( "orderLinkId", str(order.orderLinkId))
        res = self.find(MongoEndPointEnum.OPENORDERS.value, query)
        self.update(MongoEndPointEnum.OPENORDERS.value, res[0].get("_id"), order.to_dict())

    def archive_order(self, order: Order):
        logger.info(f"Arching Order To DB,OrderLinkId: {order.orderLinkId}, Symbol: {order.symbol}")
        self.add(MongoEndPointEnum.CLOSEDORDERS.value, order.to_dict())
        query = self.buildQuery( "orderLinkId", str(order.orderLinkId))
        self.deleteByQuery(MongoEndPointEnum.OPENORDERS.value, query)
    # endregion
