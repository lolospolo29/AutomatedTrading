import threading

from app.db.modules.MongoDB import MongoDB
from app.db.modules.enum.MongoEndPointEnum import MongoEndPointEnum
from app.manager.SecretsManager import SecretsManager
from app.mappers.TradeMapper import TradeMapper
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
            self._TradeMapper = TradeMapper()
            self._MongoDBTrades: MongoDB = MongoDB("Trades", self._SecretManager.returnSecret("mongodb"))
            self._initialized = True  # Markiere als initialisiert
    # endregion

    def findTradeOrTradesById(self,id:str=None)->list[Trade]:
        trades = []
        res = []
        if id is None:
            res = self._MongoDBTrades.find(MongoEndPointEnum.OPENTRADES.value,None)
        else:
            query = self._MongoDBTrades.buildQuery("Trade", "id", str(id))
            res = self._MongoDBTrades.find(MongoEndPointEnum.OPENTRADES.value, query)
        for tradeInRes in res:
            trade = self._TradeMapper.mapTradeFromDB(tradeInRes)
            orders = []
            for order in trade.orders:
                order = self.findOrderOrOrdersById(order)
                orders.append(order)
            trade.orders = []
            trade.orders.extend(orders)
            trades.append(trade)
        return trades

    def findOrderOrOrdersById(self, id: str=None) -> list[Order]:
        orders = []
        res = []
        if id is None:
            res = self._MongoDBTrades.find(MongoEndPointEnum.OPENORDERS.value, None)
        else:
            query = self._MongoDBTrades.buildQuery("Order", "orderLinkId", str(id))
            res = self._MongoDBTrades.find(MongoEndPointEnum.OPENORDERS.value, query)
        for orderInRes in res:
            orders.append(self._TradeMapper.mapOrderFromDB(orderInRes))
        return orders

    # region Add / Update / Archive
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
    # endregion

#Testing
# _mongo = mongoDBTrades()
# pd = PDArray(name="FVG",direction="Bullish")
# c1:Candle = Candle("BTC", "broker", 132.2, 132, 122, 12,datetime.datetime.now(),5)
# pd.candles.append(c1)
# pd.Ids.add(c1.id)
# level = Level("FVG",132)
# level.ids.append(c1.id)
# struct = Structure("BOS","Bullish",c1.id)
#
# order = Order()
# order.entryFrameWork = pd
# order.confirmations = []
# order.confirmations.append(pd)
# order.confirmations.append(level)
# order.confirmations.append(struct)
# order.orderLinkId = "132"
# _mongo.addOrderToDB(order)
#
# trade = Trade(AssetBrokerStrategyRelation("A","ABC","AC"),[order])
# _mongo.addTradeToDB(trade)
# _mongo.findTradeOrTradesById()