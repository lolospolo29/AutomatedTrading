import threading
from datetime import datetime

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.CandleFrameWorkDTO import CandleFrameWorkDTO
from app.db.mongodb.dtos.FrameWorkDTO import FrameWorkDTO
from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.db.mongodb.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.frameworks.FrameWork import FrameWork
from app.models.frameworks.PDArray import PDArray
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

    def find_orders(self)->list[Order]:
        orders_db:list =  self.find(MongoEndPointEnum.OPENORDERS.value, None)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_frameworks_by_orderLinkId(self,orderLinkId:str)->list[FrameWorkDTO]:
        query = self.buildQuery("orderLinkId", orderLinkId)
        frameworks_db =  self.find(MongoEndPointEnum.FRAMEWORKS.value, query)

        frameworks:list[FrameWorkDTO] = []

        for framework_db in frameworks_db:
            framework = FrameWorkDTO(**framework_db)
            frameworks.append(framework)
        return frameworks

    def find_trade_by_id(self,trade_id:str)->TradeDTO:
        query = self.buildQuery("tradeId", trade_id)
        return TradeDTO(**self.find(MongoEndPointEnum.OPENTRADES.value, query)[0])

    def find_orders_by_trade_id(self,trade_id:str)->list[Order]:
        query = self.buildQuery("tradeId", trade_id)
        orders_db =  self.find(MongoEndPointEnum.OPENORDERS.value, query)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_order_by_id(self,order_id:str)->Order:
        query = self.buildQuery("orderLinkId", order_id)
        return Order(**self.find(MongoEndPointEnum.OPENORDERS.value, query)[0])

    def find_candles_by_framework_id(self,framework_id:str)->list[CandleFrameWorkDTO]:
        query = self.buildQuery("frameWorkId", framework_id)
        candles_db =  self.find(MongoEndPointEnum.FRAMEWORKCANDLES.value, query)
        candles:list[CandleFrameWorkDTO] = []
        for candle_db in candles_db:
            candle = CandleFrameWorkDTO(**candle_db)
            candles.append(candle)
        return candles

    # region Add / Update / Archive
    def add_trade_to_db(self, trade: Trade):
        logger.info(f"Adding Trade to DB: {trade.id}")
        trade_dto:TradeDTO = self._mapper.map_trade_to_dto(trade=trade)
        self.add(MongoEndPointEnum.OPENTRADES.value,trade_dto.model_dump())

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")
        self.add(MongoEndPointEnum.OPENORDERS.value, order.model_dump(exclude={'entry_frame_work','confirmations'}))

    def add_framework_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework To DB,Name: {framework.name}")
        framework_dto:FrameWorkDTO = self._mapper.map_framework_to_dto(framework=framework)
        self.add(MongoEndPointEnum.FRAMEWORKS.value, framework_dto.model_dump())

    def add_framework_candles_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework Candles To DB,Name: {framework.name}")
        for candle in framework.candles:
            candle_dto = self._mapper.map_candle_to_dto(candle=candle,framework=framework)
            self.add(MongoEndPointEnum.FRAMEWORKCANDLES.value,
                candle_dto.model_dump())

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

    def update_framework(self, framework:FrameWork):
        logger.info(f"Update Framework To DB,Name: {framework.name}")
        query = self.buildQuery( "frameWorkId", framework.id)
        res = self.find(MongoEndPointEnum.FRAMEWORKS.value, query)
        framework_dto:FrameWorkDTO = self._mapper.map_framework_to_dto(framework=framework)
        self.update(MongoEndPointEnum.FRAMEWORKS.value, res[0].get("_id"), framework_dto.model_dump())

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


# mongo_trades = MongoDBTrades()
#
# trade = Trade(relation=Relation(asset="BTC",broker="bc",strategy="a",id=1,max_trades=1),id="31")
#
# mongo_trades.add_trade_to_db(trade)
#
# trades = mongo_trades.find_trades()
#
# candle = Candle(asset="BTC",broker="bc",open=234,high=131,low=123,close=22,iso_time=datetime.now(),timeframe=1)
#
# pd = PDArray(candles=[candle])
# pd.name = "test"
# pd.orderLinkId = "131"
#
# mongo_trades.add_framework_to_db(pd)
#
# frameworks_db = mongo_trades.find_frameworks_by_orderLinkId(pd.orderLinkId)
#
# pd.status = "a"
#
# mongo_trades.update_framework(pd)
#
# mongo_trades.add_framework_candles_to_db(pd)

