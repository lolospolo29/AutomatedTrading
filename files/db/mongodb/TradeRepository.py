from files.db.mongodb.MongoDB import MongoDB
from files.db.mongodb.dtos.BrokerDTO import BrokerDTO
from files.db.mongodb.dtos.CandleFrameWorkDTO import CandleFrameWorkDTO
from files.db.mongodb.dtos.FrameWorkDTO import FrameWorkDTO
from files.db.mongodb.dtos.TradeDTO import TradeDTO
from files.mappers.DTOMapper import DTOMapper
from files.models.frameworks.FrameWork import FrameWork
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade
from files.monitoring.logging.logging_startup import logger


class TradeRepository:

    def __init__(self, db_name:str,uri:str):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = DTOMapper()

    # endregion

    # region CRUD Trade

    def find_trades(self)->list[TradeDTO]:
        trades_db:list =  self._db.find("OpenTrades", None)

        trades:list[TradeDTO] = []

        for trade_db in trades_db:
            trade = TradeDTO(**trade_db)
            trades.append(trade)
        return trades

    def find_trade_by_id(self,trade_id:str)->TradeDTO:
        query = self._db.buildQuery("tradeId", trade_id)
        return TradeDTO(**self._db.find("OpenTrades", query)[0])

    def add_trade_to_db(self, trade: Trade):
        logger.info(f"Adding Trade to DB: {trade.id}")

        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        self._db.add("OpenTrades",trade_dto.model_dump())

    def update_trade(self, trade: Trade):
        logger.info(f"Updating Trade,OrderLinkId:{trade.id}")

        query = self._db.buildQuery( "tradeId", str(trade.id))
        res = self._db.find("OpenTrades", query)
        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        self._db.update("OpenTrades", res[0].get("_id"), trade_dto.model_dump())

    def archive_trade(self, trade: Trade):
        logger.info(f"Arching Trade,OrderLinkId:{trade.id}")

        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        self._db.add("ClosedTrades", trade_dto.model_dump())
        query = self._db.buildQuery( "tradeId", str(trade.id))
        self._db.deleteByQuery("OpenTrades", query)

    # endregion

    # region CRUD Orders
    def find_orders_by_trade_id(self,trade_id:str)->list[Order]:
        query = self._db.buildQuery("tradeId", trade_id)
        orders_db =  self._db.find("OpenOrders", query)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_orders(self)->list[Order]:
        orders_db:list =  self._db.find("OpenOrders", None)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def update_order(self, order: Order):
        logger.info(f"Update Order To DB,OrderLinkId: {order.orderLinkId},Symbol: {order.symbol}")

        query = self._db.buildQuery( "orderLinkId", str(order.orderLinkId))
        res = self._db.find("OpenOrders", query)
        self._db.update("OpenOrders", res[0].get("_id"), order.model_dump(exclude={'entry_frame_work'
                                                                                          ,'confirmations'}))

    def archive_order(self, order: Order):
        logger.info(f"Arching Order To DB,OrderLinkId: {order.orderLinkId}, Symbol: {order.symbol}")

        self._db.add("ClosedOrders", order.model_dump(exclude={'entry_frame_work','confirmations'}))
        query = self._db.buildQuery( "orderLinkId", str(order.orderLinkId))
        self._db.deleteByQuery("OpenOrders", query)

    def find_order_by_id(self,order_id:str)->Order:
        query = self._db.buildQuery("orderLinkId", order_id)
        return Order(**self._db.find("OpenOrders", query)[0])

    def add_order_to_db(self, order: Order):
        logger.info(f"Adding Order To DB,OrderLinkId: {order.orderLinkId}")

        self._db.add("OpenOrders", order.model_dump(exclude={'entry_frame_work','confirmations'}))

    # endregion

    # region FrameWork CRUD

    def find_frameworks_by_orderLinkId(self,orderLinkId:str)->list[FrameWorkDTO]:
        query = self._db.buildQuery("orderLinkId", orderLinkId)
        frameworks_db =  self._db.find("FrameWorks", query)

        frameworks:list[FrameWorkDTO] = []

        for framework_db in frameworks_db:
            framework = FrameWorkDTO(**framework_db)
            frameworks.append(framework)
        return frameworks

    def find_candles_by_framework_id(self,framework_id:str)->list[CandleFrameWorkDTO]:
        query = self._db.buildQuery("frameWorkId", framework_id)
        candles_db =  self._db.find("FrameWorkCandles", query)
        candles:list[CandleFrameWorkDTO] = []
        for candle_db in candles_db:
            candle = CandleFrameWorkDTO(**candle_db)
            candles.append(candle)
        return candles

    def add_framework_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework To DB,Name: {framework.name}")

        framework_dto:FrameWorkDTO = self._dto_mapper.map_framework_to_dto(framework=framework)
        self._db.add("FrameWorks", framework_dto.model_dump())

    def add_framework_candles_to_db(self,framework:FrameWork):
        logger.info(f"Adding Framework Candles To DB,Name: {framework.name}")

        for candle in framework.candles:
            candle_dto = self._dto_mapper.map_candle_to_dto(candle=candle, framework=framework)
            self._db.add("FrameWorkCandles",
                candle_dto.model_dump())

    def update_framework(self, framework:FrameWork):
        logger.info(f"Update Framework To DB,Name: {framework.name}")

        query = self._db.buildQuery( "frameWorkId", framework.id)
        res = self._db.find("FrameWorks", query)
        framework_dto:FrameWorkDTO = self._dto_mapper.map_framework_to_dto(framework=framework)
        self._db.update("FrameWorks", res[0].get("_id"), framework_dto.model_dump())

    # endregion

    # region Brokers R

    def find_brokers(self)->list[BrokerDTO]:
        brokers_db:list =  self._db.find("Broker", None)

        brokers_dtos:list[BrokerDTO] = []

        for broker_db in brokers_db:
            broker = BrokerDTO(**broker_db)
            brokers_dtos.append(broker)

        return brokers_dtos

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

