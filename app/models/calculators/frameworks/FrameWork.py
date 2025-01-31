from abc import abstractmethod

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation


class FrameWork:
    def __init__(self, typ):
        self.typ = typ
        self.relation = None
        self.timeframe = None

    def add_relation(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> None:
        self.relation = assetBrokerStrategyRelation

    def set_time_frame(self, timeFrame: int) -> None:
        self.timeframe = timeFrame

    @abstractmethod
    def to_dict(self):
        pass