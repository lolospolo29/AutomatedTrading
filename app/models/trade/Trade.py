from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order
import uuid

from app.monitoring.logging.logging_startup import logger


class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation=None, orders: list[Order]=None,id:str=None):
        self.orders : list[Order] = orders
        self.relation: AssetBrokerStrategyRelation = relation
        self.side = ""
        self.tpslMode = ""
        self.unrealisedPnl = 0
        self.leverage = 0
        self.size = 0
        self.tradeMode = 0
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id


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
                    "side": self.side,
                    "unrealisedPnl": self.unrealisedPnl,
                    "leverage": self.leverage,
                    "size": self.size,
                    "tradeMode": self.tradeMode,
                }
            }
        except Exception as e:
            logger.exception(e)
