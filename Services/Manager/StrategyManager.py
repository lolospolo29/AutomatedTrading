from Services.Manager.AssetManager import AssetManager

class StrategyManager:
    def __init__(self, assetManager : AssetManager):
        self.strategies: dict = {}
        self._AssetManager: AssetManager = assetManager

    def registerStrategy(self, strategy):
        self.strategies[strategy.name] = strategy
        print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")
