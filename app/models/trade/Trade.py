from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order
import uuid

class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation, orders: list[Order]):
        self.orders : list[Order] = orders
        self.relation: AssetBrokerStrategyRelation = relation
        self.id = uuid.uuid4()


    def toDict(self):
        """Gibt alle Datenpunkte als Dictionary zurück"""
        return {
            "Trade": {
                "id": str(self.id),
                "orders": [order.orderLinkId for order in self.orders],
                "asset": self.relation.asset ,
                "broker": self.relation.broker ,
                "strategy": self.relation.strategy,
            }
        }
