import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.strategy.Strategy import Strategy
from app.helper.handler.LevelHandler import LevelHandler
from app.helper.handler.PDArrayHandler import PDArrayHandler
from app.helper.handler.StructureHandler import StructureHandler


class StrategyManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(StrategyManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.strategies: dict = {}
            self._PDArrayHandler: PDArrayHandler = PDArrayHandler()
            self._LevelHandler: LevelHandler = LevelHandler()
            self._StructureHandler: StructureHandler = StructureHandler()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Register & Return

    def registerStrategy(self, strategy: Strategy) -> None:
        if strategy not in self.strategies:
            self.strategies[strategy.name] = strategy
            print(f"Strategy '{strategy.name}' created and added to the Strategy Manager.")
        else:
            print(f"Strategy '{strategy.name}' already exists in the Strategy Manager.")

    def returnExpectedTimeFrame(self, strategy: str) -> list:
        if strategy in self.strategies:
            return self.strategies[strategy].returnExpectedTimeFrame()
        return []

    # endregion

    # region FrameWork Functions

    def _updateFrameWorkHandler(self, _ids: list, relation:AssetBrokerStrategyRelation, timeFrame: int) -> bool:
        if len(_ids) <= 0:
            print("No IDs provided.")
            return True
        self._PDArrayHandler.removePDArray(_ids,relation,timeFrame)
        self._LevelHandler.removeLevel(_ids,relation,timeFrame)
        self._StructureHandler.removeStructure(_ids,relation,timeFrame)
        return True

    def _addNewFrameWorksToHandler(self, frameworks: list, relation: AssetBrokerStrategyRelation, candles: list[Candle], timeFrame: int) -> bool:
        if len(frameworks) <= 0:
            print("No frameworks provided")
            return True
        for framework in frameworks:
            framework.addRelation(relation)
            framework.setTimeFrame(timeFrame)
            if framework.typ == "PDArray":
                self._PDArrayHandler.addPDArray(framework)
                self._PDArrayHandler.addCandleToPDArrayByIds(candles, timeFrame, relation)
            if framework.typ == "Level":
                self._LevelHandler.addLevel(framework)
            if framework.typ == "Structure":
                self._StructureHandler.addStructure(framework)
        _ids = [candle.id for candle in candles]
        self._updateFrameWorkHandler(_ids, relation, timeFrame)
        return True

    # endregion

    # region strategy Functions
    def analyzeStrategy(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                        timeFrame: int) -> None:
            if len(candles) <= 0:
                return None
            if relation.strategy in self.strategies:
                frameworks:list = self.strategies[relation.strategy].analyzeData(candles,timeFrame)
                self._addNewFrameWorksToHandler(frameworks, relation, candles, timeFrame)

    def getEntry(self, candles: list[Candle], relation: AssetBrokerStrategyRelation,
                        timeFrame: int):
        if len (candles) <= 0:
            return None
        if relation.strategy in self.strategies:
            self._PDArrayHandler.updatePDArrays(candles, timeFrame, relation)
            pd: list = self._PDArrayHandler.returnPDArrays(relation)
            level: list = self._LevelHandler.returnLevels(relation)
            structure: list = self._StructureHandler.returnStructure(relation)


            self.strategies[relation.strategy].getEntry(candles,timeFrame,pd,level,structure)
    # endregion