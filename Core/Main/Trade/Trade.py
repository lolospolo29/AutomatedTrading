from Core.Main.Asset.SubModels.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Core.Main.Trade import Order


class Trade:

    def __init__(self, relation: AssetBrokerStrategyRelation):
        self.orders : list[Order] = []
        self.relation: AssetBrokerStrategyRelation = relation
        self.duration: float = 0
        self.openTime: str = ""
        self.closeTime: str = ""
