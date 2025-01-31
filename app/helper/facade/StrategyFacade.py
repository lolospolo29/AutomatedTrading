from numpy.distutils.fcompiler import none

from app.helper.calculator.PDRiskCalculator import PDRiskCalculator
from app.helper.calculator.PositionSizeCalculator import PositionSizeCalculator
from app.helper.calculator.ProfitStopAnalyzer import ProfitStopAnalyzer
from app.helper.calculator.RiskCalculator import RiskCalculator
from app.helper.handler.LevelHandler import LevelHandler
from app.helper.handler.PDArrayHandler import PDArrayHandler
from app.helper.handler.SMTHandler import SMTHandler
from app.helper.handler.StructureHandler import StructureHandler
from app.helper.mediator.LevelMediator import LevelMediator
from app.helper.mediator.PDMediator import PDMediator
from app.helper.mediator.StructureMediator import StructureMediator


class StrategyFacade:
    def __init__(self,asset1:str=none,asset2:str=none,correlation:str=none):

        self.PDMediator = PDMediator()
        self.StructureMediator:StructureMediator = StructureMediator()
        self.LevelMediator: LevelMediator = LevelMediator()


        self.pd_array_handler = PDArrayHandler()
        self.structure_handler = StructureHandler()
        self.level_handler = LevelHandler()

        self.Risk_Calculator: RiskCalculator = RiskCalculator()
        self.pd_risk_calculator = PDRiskCalculator()
        self.profit_stop_analyzer = ProfitStopAnalyzer()
        self.position_size_calculator = PositionSizeCalculator()

        self.smt_handler = None
        if asset1 and asset2 and correlation:
            self.smt_handler = SMTHandler(asset1,asset2,correlation)
