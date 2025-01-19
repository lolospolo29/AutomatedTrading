from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade


class TradeBuilder:
    def __init__(self):
        self._Trade = Trade()

    def add_relation(self, relation:AssetBrokerStrategyRelation):
        self._Trade.relation = relation
        return self

    def add_order(self, order:Order):
        if self._Trade.orders is None:
            self._Trade.orders = []
        self._Trade.orders.append(order)
        return self

    def add_orders(self, orders:list[Order]):
        if self._Trade.orders is None:
            self._Trade.orders = []
        for order in orders:
            self.add_order(order)
        return self

    def add_side(self, side:str):
        self._Trade.side = side
        return self

    def add_tpsl_mode(self, tpslMode:str):
        self._Trade.tpslMode = tpslMode
        return self

    def build(self):
        return self._Trade

tb = TradeBuilder().add_side("ada")
print(tb.build())