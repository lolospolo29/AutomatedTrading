from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.Main.Asset.Candle import Candle
from Models.Main.Strategies.Strategy import Strategy
from Services.Manager.AssetManager import AssetManager

class StrategyManager:
    def __init__(self, assetManager : AssetManager):
        self.strategies: dict = {}
        self._AssetManager: AssetManager = assetManager

    def registerStrategy(self, strategy: Strategy):
        self.strategies[strategy.name] = strategy
        print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")

    def returnDataDuration(self, strategy: str) -> int:
        if strategy not in self.strategies:
            return self.strategies[strategy].returnDataDuration()

    def returnExpectedTimeFrame(self, strategy: str) -> list:
        if strategy in self.strategies:
            return self.strategies[strategy].returnExpectedTimeFrame()
        return []

    def returnDataDuration(self,strategy: str) -> int:
        if strategy in self.strategies:
            return self.strategies[strategy].returnDataDuration()

    def analyzeStrategy(self, candles: list[Candle], relations: list[AssetBrokerStrategyRelation],
                        timeFrame: int) -> None:
        for relation in relations:
            if relation.strategy in self.strategies:
                frameworks:list = self.strategies[relation.strategy].analyzeData(candles)