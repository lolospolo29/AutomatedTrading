from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order
import uuid

from app.monitoring.logging.logging_startup import logger


class Trade:

    def __init__(self,relation: AssetBrokerStrategyRelation = None, id: str = None,
                 category: str = None):
        self.orders : list = []
        self.relation: AssetBrokerStrategyRelation = relation

        if id is None:
            self.id: str = str(uuid.uuid4())
        else:
            self.id:str = id

        self.category:str = category
        self.side:str = ""
        self.tpslMode:str = ""
        self.unrealisedPnl:str = ""
        self.leverage:str = ""
        self.size:str = ""
        self.tradeMode:int = 0
        self.updatedTime:str = ""
        self.createdTime:str = ""

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
                    "id": self.id,  # Ensure string format
                    "orders": self.orders,  # Ensure list
                    "asset": self.relation.asset,  # Use default empty string
                    "broker": self.relation.broker,
                    "strategy": self.relation.strategy,
                    "category": self.category,
                    "side": self.side,
                    "tpslMode": self.tpslMode,
                    "unrealisedPnl": self.unrealisedPnl,
                    "leverage": self.leverage,  # Default leverage to 1
                    "size": self.size,
                    "tradeMode": self.tradeMode,
                    "updatedTime": self.updatedTime,
                    "createdTime": self.createdTime,
            }
        except Exception as e:
            logger.exception("Mapping Error with TradeId: {tradeId},Error:{error}".format(tradeId=self.id,error=e))
