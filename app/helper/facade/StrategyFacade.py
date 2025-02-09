from numpy.distutils.fcompiler import none
from pydantic import BaseModel

from app.helper.calculator.entry.PDStopEntryCalculator import PDStopEntryCalculator
from app.helper.calculator.RiskCalculator import RiskCalculator
from app.helper.calculator.entry.ProfitStopEntrySorter import ProfitStopEntrySorter
from app.helper.calculator.entry.ProfitStopEntryCalculator import ProfitStopEntryCalculator
from app.helper.handler.LevelHandler import LevelHandler
from app.helper.handler.PDArrayHandler import PDArrayHandler
from app.helper.handler.SMTHandler import SMTHandler
from app.helper.handler.StructureHandler import StructureHandler
from app.helper.mediator.LevelMediator import LevelMediator
from app.helper.mediator.PDMediator import PDMediator
from app.helper.mediator.StructureMediator import StructureMediator


class StrategyFacade:
    """
    Facilitates interaction between various mediators and handlers to implement
    complex strategies combining multiple components.

    The StrategyFacade class serves as a single point of access for complex
    functionalities provided by different components such as mediators, handlers,
    and calculators. It simplifies orchestration by aggregating these components
    and providing modular, scalable implementation for strategies involving
    multiple assets and their correlations. If asset information and correlation
    are provided, an SMTHandler will also be initialized for further operations.

    """
    def __init__(self,asset1:str=None,asset2:str=None,correlation:str=None):

        self.PDMediator = PDMediator()
        self.StructureMediator:StructureMediator = StructureMediator()
        self.LevelMediator: LevelMediator = LevelMediator()


        self.pd_array_handler = PDArrayHandler()
        self.structure_handler = StructureHandler()
        self.level_handler = LevelHandler()

        self.smt_handler = None
        if asset1 and asset2 and correlation:
            self.smt_handler = SMTHandler(asset1,asset2,correlation)

        self.risk_calculator = RiskCalculator()

        self.profit_stop_entry_calculator: ProfitStopEntryCalculator = ProfitStopEntryCalculator()
        self.profit_stop_entry_sorter = ProfitStopEntrySorter()
        self.pd_stop_entry_calculator = PDStopEntryCalculator()
