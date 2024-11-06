from Models.Main.Strategies.Strategy import Strategy
from Services.Manager.AssetManager import AssetManager

class StrategyManager:
    def __init__(self, assetManager : AssetManager):
        self.strategies: dict = {}
        self._AssetManager: AssetManager = assetManager

    def registerStrategy(self, strategy: Strategy):
        self.strategies[strategy.name] = strategy
        print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")

    def returnExpectedTimeFrame(self, strategy: str) -> list:
        if strategy in self.strategies:
            return self.strategies[strategy].returnExpectedTimeFrame()
        return []
