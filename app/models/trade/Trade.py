from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.trade import Order


class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation, orders: list[Order]):
        self.orders : list[Order] = []
        self.relation: AssetBrokerStrategyRelation = relation
        self.timeFrame: int = 0
