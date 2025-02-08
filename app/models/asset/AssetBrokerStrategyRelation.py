class AssetBrokerStrategyRelation:
    def __init__(self, asset: str, broker: str, strategy: str, max_trades:int=1):
        self.asset = asset
        self.broker = broker
        self.strategy = strategy
        self.max_trades = max_trades

    def compare(self, assetBrokerStrategyRelation: "AssetBrokerStrategyRelation") -> bool:
        if (self.asset == assetBrokerStrategyRelation.asset and self.broker == assetBrokerStrategyRelation.broker and
                self.strategy == assetBrokerStrategyRelation.strategy):
            return True
        return False

    def __str__(self):
        return f"{self.asset} {self.broker} {self.strategy}"

    def to_dict(self) -> dict:
        return {
                "asset": self.asset,
                "broker": self.broker,
                "strategy": self.strategy,
                "max_trades": self.max_trades
        }