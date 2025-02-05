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
        """Gibt alle Datenpunkte als Dictionary zurück, selbst wenn Werte fehlen"""
        try:
            return {
                "Trade": {
                    "id": str(self.id) if self.id else "",  # Ensure string format
                    "orders": [order.orderLinkId for order in (self.orders or [])],  # Ensure list
                    "asset": getattr(self.relation, "asset", ""),  # Use default empty string
                    "broker": getattr(self.relation, "broker", ""),
                    "strategy": getattr(self.relation, "strategy", ""),
                    "category": self.category if self.category is not None else "",
                    "side": self.side if self.side is not None else "",
                    "tpslMode": self.tpslMode if self.tpslMode is not None else "",
                    "unrealisedPnl": self.unrealisedPnl if self.unrealisedPnl is not None else 0.0,
                    # Default to 0.0 for numbers
                    "leverage": self.leverage if self.leverage is not None else 1,  # Default leverage to 1
                    "size": self.size if self.size is not None else 0,
                    "tradeMode": self.tradeMode if self.tradeMode is not None else "",
                    "updatedTime": self.updatedTime if self.updatedTime is not None else "",
                    "createdTime": self.createdTime if self.createdTime is not None else "",
                }
            }
        except Exception as e:
            logger.exception("Mapping Error with TradeId: {tradeId},Error:{error}".format(tradeId=self.id,error=e))
