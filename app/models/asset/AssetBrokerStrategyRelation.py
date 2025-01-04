class AssetBrokerStrategyRelation:
    def __init__(self, asset: str,broker: str, strategy: str,maxTrades:int):
        self.asset = asset
        self.broker = broker
        self.strategy = strategy
        self.maxTrades = maxTrades

    def compare(self, assetBrokerStrategyRelation: "AssetBrokerStrategyRelation") -> bool:
        if (self.asset == assetBrokerStrategyRelation.asset and self.broker == assetBrokerStrategyRelation.broker and
                self.strategy == assetBrokerStrategyRelation.strategy):
            return True
        return False

    def __str__(self):
        return self.asset + self.broker + self.strategy

