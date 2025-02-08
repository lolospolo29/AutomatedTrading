import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.ClassMapper import ClassMapper
from app.mappers.TradeMapper import TradeMapper
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


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
            self._secret_manager: SecretsManager = SecretsManager()
            self._trade_mapper = TradeMapper()
            self._class_mapper = ClassMapper()

            self._mongo_db_trades: MongoDB = MongoDB("Trades", self._secret_manager.return_secret("mongodb"))
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def find_trade_or_trades_by_id(self, id: str = None) -> list[Trade]:
        trades = []
        if id is None:
            res = self._mongo_db_trades.find(MongoEndPointEnum.OPENTRADES.value, None)
        else:
            query = self._mongo_db_trades.buildQuery("id", str(id))
            logger.info("Finding Trades in DB with Query: {}".format(query))
            res = self._mongo_db_trades.find(MongoEndPointEnum.OPENTRADES.value, query)
            logger.debug("Found Trades:{count}".format(count=len(res)))
        for tradeInRes in res:
            trade = self._trade_mapper.map_trade_from_db(tradeInRes)
            orders = []
            for _ids in trade.orders:
                res = self.find_order_or_orders_by_id(_ids)
                orders.extend(res)
            trade.orders = []
            trade.orders.extend(orders)
            trades.append(trade)
        return trades

    def find_order_or_orders_by_id(self, id: str = None) -> list[Order]:
        orders = []
        res = []
        if id is None:
            res = self._mongo_db_trades.find(MongoEndPointEnum.OPENORDERS.value, None)
        else:
            query = self._mongo_db_trades.buildQuery("orderLinkId", str(id))
            res = self._mongo_db_trades.find(MongoEndPointEnum.OPENORDERS.value, query)
        for orderInRes in res:
                orders.append(self._trade_mapper.map_order_from_db(orderInRes))
        return orders

    # region Add / Update / Archive
    def add_trade_to_db(self, trade: Trade):
        logger.info(f"Adding Trade to DB: {trade.id}")
        self._mongo_db_trades.add(MongoEndPointEnum.OPENTRADES.value, trade.to_dict())

    def update_trade(self, trade: Trade):
        logger.info(f"Updating Trade,OrderLinkId:{trade.id}")
        query = self._mongo_db_trades.buildQuery( "id", str(trade.id))
        res = self._mongo_db_trades.find(MongoEndPointEnum.OPENTRADES.value, query)
        self._mongo_db_trades.update(MongoEndPointEnum.OPENTRADES.value, res[0].get("_id"), trade.to_dict())

    def archive_trade(self, trade: Trade):
        logger.info(f"Arching Trade,OrderLinkId:{trade.id}")
        self._mongo_db_trades.add(MongoEndPointEnum.CLOSEDTRADES.value, trade.to_dict())
        query = self._mongo_db_trades.buildQuery( "id", str(trade.id))
        self._mongo_db_trades.deleteByQuery(MongoEndPointEnum.OPENTRADES.value, query)

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")
        self._mongo_db_trades.add(MongoEndPointEnum.OPENORDERS.value, order.to_dict())

    def update_order(self, order: Order):
        logger.info(f"Update Order To DB,OrderLinkId: {order.orderLinkId},Symbol: {order.symbol}")

        query = self._mongo_db_trades.buildQuery( "orderLinkId", str(order.orderLinkId))
        res = self._mongo_db_trades.find(MongoEndPointEnum.OPENORDERS.value, query)
        self._mongo_db_trades.update(MongoEndPointEnum.OPENORDERS.value, res[0].get("_id"), order.to_dict())

    def archive_order(self, order: Order):
        logger.info(f"Arching Order To DB,OrderLinkId: {order.orderLinkId}, Symbol: {order.symbol}")
        self._mongo_db_trades.add(MongoEndPointEnum.CLOSEDORDERS.value, order.to_dict())
        query = self._mongo_db_trades.buildQuery( "orderLinkId", str(order.orderLinkId))
        self._mongo_db_trades.deleteByQuery(MongoEndPointEnum.OPENORDERS.value, query)
    # endregion
# todo db testing