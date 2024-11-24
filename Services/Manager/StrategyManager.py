from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.Main.Asset.Candle import Candle
from Models.Main.Strategies.Strategy import Strategy
from Services.Manager.AssetManager import AssetManager
from Services.Manager.StrategyHandler.LevelHandler import LevelHandler
from Services.Manager.StrategyHandler.PDArrayHandler import PDArrayHandler
from Services.Manager.StrategyHandler.StructureHandler import StructureHandler


class StrategyManager:
    def __init__(self, assetManager : AssetManager, pdArrayHandler: PDArrayHandler, levelHandler: LevelHandler,
                 structureHandler: StructureHandler):
        self.strategies: dict = {}
        self._AssetManager: AssetManager = assetManager
        self._PDArrayHandler: PDArrayHandler = pdArrayHandler
        self._LevelHandler: LevelHandler = levelHandler
        self._StructureHandler: StructureHandler = structureHandler

    def registerStrategy(self, strategy: Strategy) -> None:
        self.strategies[strategy.name] = strategy
        print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")

    def returnExpectedTimeFrame(self, strategy: str) -> list:
        if strategy in self.strategies:
            return self.strategies[strategy].returnExpectedTimeFrame()
        return []

    def returnDuration(self,strategy: str) -> int:
        if strategy in self.strategies:
            return self.strategies[strategy].returnDataDuration()

    def updateFrameWorkHandler(self,_ids: list,relation:AssetBrokerStrategyRelation,timeFrame: int ) -> None:
        if len(_ids) <= 0:
            return None
        self._PDArrayHandler.removePDArray(_ids,relation,timeFrame)
        self._LevelHandler.removeLevel(_ids,relation,timeFrame)
        self._StructureHandler.removeStructure(_ids,relation,timeFrame)

    def analyzeStrategy(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                        timeFrame: int) -> None:
            if len(candles) < 10:
                return None
            if relation.strategy in self.strategies:
                frameworks:list = self.strategies[relation.strategy].analyzeData(candles,timeFrame)
                if len(frameworks) <= 0:
                    return None
                for framework in frameworks:
                    framework.addRelation(relation)
                    framework.setTimeFrame(timeFrame)
                    if framework.typ == "PDArray":
                        self._PDArrayHandler.addPDArray(framework)
                        self._PDArrayHandler.addCandleToPDArrayByIds(candles,timeFrame,relation)
                    if framework.typ == "Level":
                        self._LevelHandler.addLevel(framework)
                    if framework.typ == "Structure":
                        self._StructureHandler.addStructure(framework)


    def getEntry(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                        timeFrame: int):

        if len (candles) < 10:
            return None
        if relation.strategy in self.strategies:
            pd: list = self._PDArrayHandler.returnPDArrays(relation)
            level: list = self._LevelHandler.returnLevels(relation)
            structure: list = self._StructureHandler.returnStructure(relation)

            self.strategies[relation.strategy].getEntry(candles,timeFrame,pd,level,structure)