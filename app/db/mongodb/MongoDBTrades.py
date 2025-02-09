import threading

from app.mappers.DTOMapper import DTOMapper
from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.db.mongodb.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.initializer.SecretsManager import SecretsManager
from app.models.asset.Relation import Relation
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
            self._mapper:DTOMapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def find_trades(self)->list[TradeDTO]:
        trades_db:list =  self.find(MongoEndPointEnum.OPENTRADES.value, None)

        trades:list[TradeDTO] = []

        for trade_db in trades_db:
            trade = TradeDTO(**trade_db)
            trades.append(trade)
        return trades

    def find_trade_by_id(self,trade_id:str)->TradeDTO:
        query = self.buildQuery("tradeId", trade_id)
        return TradeDTO(**self.find(MongoEndPointEnum.OPENTRADES.value, query)[0])

    def find_orders(self)->list[Order]:
        orders_db:list =  self.find(MongoEndPointEnum.OPENORDERS.value, None)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_order_by_id(self,order_id:str)->Order:
        query = self.buildQuery("orderLinkId", order_id)
        return Order(**self.find(MongoEndPointEnum.OPENORDERS.value, query)[0])

    # region Add / Update / Archive
    def add_trade_to_db(self, trade: Trade):
        trade_dto:TradeDTO = self._mapper.map_trade_to_dto(trade=trade)
        logger.info(f"Adding Trade to DB: {trade.id}")
        self.add(MongoEndPointEnum.OPENTRADES.value,trade_dto.model_dump())

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")
        self.add(MongoEndPointEnum.OPENORDERS.value, order.model_dump(exclude={'entry_frame_work','confirmations'}))

    def update_trade(self, trade: Trade):
        logger.info(f"Updating Trade,OrderLinkId:{trade.id}")
        query = self.buildQuery( "tradeId", str(trade.id))
        res = self.find(MongoEndPointEnum.OPENTRADES.value, query)

        trade_dto:TradeDTO = self._mapper.map_trade_to_dto(trade=trade)

        self.update(MongoEndPointEnum.OPENTRADES.value, res[0].get("_id"), trade_dto.model_dump())

    def update_order(self, order: Order):
        logger.info(f"Update Order To DB,OrderLinkId: {order.orderLinkId},Symbol: {order.symbol}")

        query = self.buildQuery( "orderLinkId", str(order.orderLinkId))
        res = self.find(MongoEndPointEnum.OPENORDERS.value, query)
        self.update(MongoEndPointEnum.OPENORDERS.value, res[0].get("_id"), order.model_dump(exclude={'entry_frame_work','confirmations'}))

    def archive_trade(self, trade: Trade):
        logger.info(f"Arching Trade,OrderLinkId:{trade.id}")

        trade_dto:TradeDTO = self._mapper.map_trade_to_dto(trade=trade)

        self.add(MongoEndPointEnum.CLOSEDTRADES.value, trade_dto.model_dump())
        query = self.buildQuery( "tradeId", str(trade.id))
        self.deleteByQuery(MongoEndPointEnum.OPENTRADES.value, query)

    def archive_order(self, order: Order):
        logger.info(f"Arching Order To DB,OrderLinkId: {order.orderLinkId}, Symbol: {order.symbol}")
        self.add(MongoEndPointEnum.CLOSEDORDERS.value, order.model_dump(exclude={'entry_frame_work','confirmations'}))
        query = self.buildQuery( "orderLinkId", str(order.orderLinkId))
        self.deleteByQuery(MongoEndPointEnum.OPENORDERS.value, query)
    # endregion


mongo_trades = MongoDBTrades()
