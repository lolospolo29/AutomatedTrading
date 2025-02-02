from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order
import uuid

from app.monitoring.logging.logging_startup import logger


class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation=None, orders: list[Order]=None,id:str=None,category:str=None):
        self.orders : list[Order] = orders
        self.relation: AssetBrokerStrategyRelation = relation

        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id

        self.category = category
        self.side = ""
        self.tpslMode = ""
        self.unrealisedPnl = 0
        self.leverage = 0
        self.size = 0
        self.tradeMode = 0
        self.updatedTime = 0
        self.createdTime = 0
        self.positionValue = 0

    def add_order(self, order: Order):
        if self.orders is None:
            self.orders = []
        if self.orders is not None:
            self.orders.append(order)
    def add_orders(self, orders: list[Order]):
        if self.orders is None:
            self.orders = []
        if self.orders is not None:
            self.orders.extend(orders)

    def to_dict(self):
        """Gibt alle Datenpunkte als Dictionary zurück"""
        try:
            return {
                "Trade": {
                    "id": str(self.id),
                    "orders": [order.orderLinkId for order in self.orders],
                    "asset": self.relation.asset ,
                    "broker": self.relation.broker ,
                    "strategy": self.relation.strategy ,
                    "category": self.category ,
                    "side": self.side,
                    "tpslMode": self.tpslMode,
                    "unrealisedPnl": self.unrealisedPnl,
                    "leverage": self.leverage,
                    "size": self.size,
                    "tradeMode": self.tradeMode,
                    "updatedTime": self.updatedTime,
                    "createdTime": self.createdTime,
                }
            }
        except Exception as e:
            logger.exception("Mapping Error with TradeId: {tradeId},Error:{error}".format(tradeId=self.id,error=e))
