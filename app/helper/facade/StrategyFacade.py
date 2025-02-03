from numpy.distutils.fcompiler import none

from app.models.calculators.PDStopEntryCalculator import PDStopEntryCalculator
from app.helper.calculator.RiskCalculator import RiskCalculator
from app.models.calculators.ProfitStopEntrySorter import ProfitStopEntrySorter
from app.models.calculators.ProfitStopEntryCalculator import ProfitStopEntryCalculator
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

    :ivar PDMediator: Mediates operations related to price and data.
    :type PDMediator: PDMediator
    :ivar StructureMediator: Handles structure-related interactions and processes.
    :type StructureMediator: StructureMediator
    :ivar LevelMediator: Manages levels and level-specific functionality.
    :type LevelMediator: LevelMediator
    :ivar pd_array_handler: Processes array-based data in the context of price
        and data functionality.
    :type pd_array_handler: PDArrayHandler
    :ivar structure_handler: Provides tools and methods for handling structures.
    :type structure_handler: StructureHandler
    :ivar level_handler: Handles functionality and operations tied to specific
        levels.
    :type level_handler: LevelHandler
    :ivar profit_stop_entry_calculator: Calculates entries for profit stop
        strategies.
    :type profit_stop_entry_calculator: ProfitStopEntryCalculator
    :ivar profit_stop_entry_sorter: Analyzes and sorts profit stop outcomes.
    :type profit_stop_entry_sorter: ProfitStopEntrySorter
    :ivar risk_calculator: Determines optimal position sizes for trading
        or investment.
    :type risk_calculator: RiskCalculator
    :ivar smt_handler: Handles strategies involving multiple assets and their
        specified correlation, initialized only if asset1, asset2, and correlation
        are provided.
    :type smt_handler: SMTHandler or None
    """
    def __init__(self,asset1:str=none,asset2:str=none,correlation:str=none):

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
