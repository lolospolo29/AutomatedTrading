import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.CandleFrameWorkDTO import CandleFrameWorkDTO
from app.db.mongodb.dtos.FrameWorkDTO import FrameWorkDTO
from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.db.mongodb.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from app.models.frameworks.FrameWork import FrameWork
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class TradeRepository:
    # region Initializing
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradeRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            self.__secret = self._secret_manager.return_secret("mongodb")
            self._dto_mapper:DTOMapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def find_trades(self)->list[TradeDTO]:
        db = MongoDB(dbName="Trades",uri=self.__secret)
        trades_db:list =  db.find(MongoEndPointEnum.OPENTRADES.value, None)

        trades:list[TradeDTO] = []

        for trade_db in trades_db:
            trade = TradeDTO(**trade_db)
            trades.append(trade)
        return trades

    def find_orders(self)->list[Order]:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        orders_db:list =  db.find(MongoEndPointEnum.OPENORDERS.value, None)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_frameworks_by_orderLinkId(self,orderLinkId:str)->list[FrameWorkDTO]:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        query = db.buildQuery("orderLinkId", orderLinkId)
        frameworks_db =  db.find(MongoEndPointEnum.FRAMEWORKS.value, query)

        frameworks:list[FrameWorkDTO] = []

        for framework_db in frameworks_db:
            framework = FrameWorkDTO(**framework_db)
            frameworks.append(framework)
        return frameworks

    def find_trade_by_id(self,trade_id:str)->TradeDTO:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        query = db.buildQuery("tradeId", trade_id)
        return TradeDTO(**db.find(MongoEndPointEnum.OPENTRADES.value, query)[0])

    def find_orders_by_trade_id(self,trade_id:str)->list[Order]:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        query = db.buildQuery("tradeId", trade_id)
        orders_db =  db.find(MongoEndPointEnum.OPENORDERS.value, query)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_order_by_id(self,order_id:str)->Order:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        query = db.buildQuery("orderLinkId", order_id)
        return Order(**db.find(MongoEndPointEnum.OPENORDERS.value, query)[0])

    def find_candles_by_framework_id(self,framework_id:str)->list[CandleFrameWorkDTO]:
        db = MongoDB(dbName="Trades",uri=self.__secret)

        query = db.buildQuery("frameWorkId", framework_id)
        candles_db =  db.find(MongoEndPointEnum.FRAMEWORKCANDLES.value, query)
        candles:list[CandleFrameWorkDTO] = []
        for candle_db in candles_db:
            candle = CandleFrameWorkDTO(**candle_db)
            candles.append(candle)
        return candles

    # region Add / Update / Archive
    def add_trade_to_db(self, trade: Trade):
        logger.info(f"Adding Trade to DB: {trade.id}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        db.add(MongoEndPointEnum.OPENTRADES.value,trade_dto.model_dump())

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        db.add(MongoEndPointEnum.OPENORDERS.value, order.model_dump(exclude={'entry_frame_work','confirmations'}))

    def add_framework_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework To DB,Name: {framework.name}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        framework_dto:FrameWorkDTO = self._dto_mapper.map_framework_to_dto(framework=framework)
        db.add(MongoEndPointEnum.FRAMEWORKS.value, framework_dto.model_dump())

    def add_framework_candles_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework Candles To DB,Name: {framework.name}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        for candle in framework.candles:
            candle_dto = self._dto_mapper.map_candle_to_dto(candle=candle, framework=framework)
            db.add(MongoEndPointEnum.FRAMEWORKCANDLES.value,
                candle_dto.model_dump())

    def update_trade(self, trade: Trade):
        logger.info(f"Updating Trade,OrderLinkId:{trade.id}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        query = db.buildQuery( "tradeId", str(trade.id))
        res = db.find(MongoEndPointEnum.OPENTRADES.value, query)
        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        db.update(MongoEndPointEnum.OPENTRADES.value, res[0].get("_id"), trade_dto.model_dump())

    def update_order(self, order: Order):
        logger.info(f"Update Order To DB,OrderLinkId: {order.orderLinkId},Symbol: {order.symbol}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        query = db.buildQuery( "orderLinkId", str(order.orderLinkId))
        res = db.find(MongoEndPointEnum.OPENORDERS.value, query)
        db.update(MongoEndPointEnum.OPENORDERS.value, res[0].get("_id"), order.model_dump(exclude={'entry_frame_work'
                                                                                          ,'confirmations'}))

    def update_framework(self, framework:FrameWork):
        logger.info(f"Update Framework To DB,Name: {framework.name}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        query = db.buildQuery( "frameWorkId", framework.id)
        res = db.find(MongoEndPointEnum.FRAMEWORKS.value, query)
        framework_dto:FrameWorkDTO = self._dto_mapper.map_framework_to_dto(framework=framework)
        db.update(MongoEndPointEnum.FRAMEWORKS.value, res[0].get("_id"), framework_dto.model_dump())

    def archive_trade(self, trade: Trade):
        logger.info(f"Arching Trade,OrderLinkId:{trade.id}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        db.add(MongoEndPointEnum.CLOSEDTRADES.value, trade_dto.model_dump())
        query = db.buildQuery( "tradeId", str(trade.id))
        db.deleteByQuery(MongoEndPointEnum.OPENTRADES.value, query)

    def archive_order(self, order: Order):
        logger.info(f"Arching Order To DB,OrderLinkId: {order.orderLinkId}, Symbol: {order.symbol}")

        db = MongoDB(dbName="Trades",uri=self.__secret)
        db.add(MongoEndPointEnum.CLOSEDORDERS.value, order.model_dump(exclude={'entry_frame_work','confirmations'}))
        query = db.buildQuery( "orderLinkId", str(order.orderLinkId))
        db.deleteByQuery(MongoEndPointEnum.OPENORDERS.value, query)
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

