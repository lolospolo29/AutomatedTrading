from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation


class FrameWork:
    def __init__(self, typ):
        self.typ = typ
        self.assetBrokerStrategyRelation = None
        self.timeFrame = None

    def addRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> None:
        self.assetBrokerStrategyRelation = assetBrokerStrategyRelation
    def setTimeFrame(self, timeFrame: int) -> None:
        self.timeFrame = timeFrame