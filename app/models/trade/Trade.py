from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order
import uuid

class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation, orders: list[Order]):
        self.orders : list[Order] = orders
        self.relation: AssetBrokerStrategyRelation = relation
        self.side = ""
        self.tpslMode = ""
        self.unrealisedPnl = 0
        self.leverage = 0
        self.size = 0
        self.tradeMode = 0
        self.id = uuid.uuid4()
    # todo file trade logging


    def toDict(self):
        """Gibt alle Datenpunkte als Dictionary zurück"""
        return {
            "Trade": {
                "id": str(self.id),
                "orders": [order.orderLinkId for order in self.orders],
                "asset": self.relation.asset ,
                "broker": self.relation.broker ,
                "side": self.side,
                "unrealisedPnl": self.unrealisedPnl,
                "leverage": self.leverage,
                "size": self.size,
                "tradeMode": self.tradeMode,
            }
        }
