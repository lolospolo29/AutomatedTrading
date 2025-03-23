from files.db.MongoDB import MongoDB
from files.models.frameworks.FrameWork import FrameWork
from files.models.trade.Broker import Broker
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade

class TradeRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Trade

    def add_trade(self, trade: Trade):
        self._db.add("OpenTrades",trade.model_dump(exclude={"id"}))

    def find_trades(self)->list[Trade]:
        trades_db:list =  self._db.find("OpenTrades", None)

        trades:list[Trade] = []

        for trade_db in trades_db:
            trade = Trade(**trade_db)
            trades.append(trade)
        return trades

    def find_trade_by_id(self, id:str)->Trade:
        query = self._db.build_query("tradeId", id)
        return Trade(**self._db.find("OpenTrades", query)[0])

    def update_trade(self, trade: Trade):
        dto = self.find_trade_by_id(trade.trade_id)
        self._db.update("OpenTrades",str(dto.id), trade.model_dump(exclude={"id"}))

    # endregion

    # region Order

    def add_order_to_db(self, order: Order):
        self._db.add("OpenOrders", order.model_dump(exclude={'id','entry_frame_work', 'confirmations'}))

    def find_orders(self)->list[Order]:
        orders_db:list =  self._db.find("OpenOrders", None)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def find_order_by_id(self,order_id:str)->Order:
        query = self._db.build_query("orderLinkId", order_id)
        return Order(**self._db.find("OpenOrders", query)[0])

    def find_orders_by_trade_id(self,trade_id:str)->list[Order]:
        query = self._db.build_query("tradeId", trade_id)
        orders_db =  self._db.find("OpenOrders", query)
        orders:list[Order] = []
        for order_db in orders_db:
            order = Order(**order_db)
            orders.append(order)
        return orders

    def update_order(self, order: Order):
        dto = self.find_order_by_id(order.order_id)
        self._db.update("OpenOrders",dto.id , order.model_dump(exclude={'id','entry_frame_work', 'confirmations'}))

    # endregion

    # region FrameWork

    def add_framework_to_db(self, framework:FrameWork):
        self._db.add("FrameWorks", framework.model_dump(exclude={"id"}))

    def find_frameworks_by_orderLinkId(self,orderLinkId:str)->list[FrameWork]:
        query = self._db.build_query("orderLinkId", orderLinkId)
        frameworks_db =  self._db.find("FrameWorks", query)

        frameworks:list[FrameWork] = []

        for framework_db in frameworks_db:
            framework = FrameWork(**framework_db)
            frameworks.append(framework)
        return frameworks

    def update_framework(self, framework:FrameWork):
        dto = self.find_trade_by_id(framework.tradeId)
        self._db.update("FrameWorks",dto.id , framework.model_dump(exclude={"id"}))

    # endregion

    # region Brokers

    def find_brokers(self)->list[Broker]:
        brokers_db:list =  self._db.find("Broker", None)

        brokers_dtos:list[Broker] = []

        for broker_db in brokers_db:
            broker = Broker(**broker_db)
            brokers_dtos.append(broker)

        return brokers_dtos

    # endregion