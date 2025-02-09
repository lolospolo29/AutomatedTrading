from app.helper.calculator.time.London import LondonOpen
from app.helper.calculator.time.NYOpen import NYOpen
from app.helper.calculator.time.macro.quarter.FirstQuarterWindow import FirstQuarterWindow
from app.helper.calculator.time.macro.quarter.LastQuarterWindow import LastQuarterWindow
from app.helper.calculator.time.macro.silverBullet.SilverBulletLondon import SilverBulletLondon
from app.helper.facade.StrategyFacade import StrategyFacade
from app.helper.handler.SMTHandler import SMTHandler
from app.helper.strategy.DoubleFib import DoubleFib
from app.helper.strategy.FVGSession import FVGSession
from app.helper.strategy.LondonSB import LondonSB
from app.helper.strategy.OTEFourH import OTEFourH
from app.helper.strategy.TestSMT import TestSMTStrategy
from app.helper.strategy.Unicorn import Unicorn
from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.monitoring.logging.logging_startup import logger


class StrategyFactory:
    def return_strategy(self, typ: str) -> Strategy:
        if typ == "FVGSession":
            fvg =  FVGSession(name="FVGSession", timeframes=[ExpectedTimeFrame(timeframe=1, max_Len=90)]
                              ,strategy_facade=StrategyFacade())
            return fvg
        if typ == "Unicorn":
            gen_timeframes = self.generate_timeframes([240, 5], [1, 90])
            unicorn =  Unicorn(name="Unicorn", timeframes=gen_timeframes, time_windows=[LondonOpen(), NYOpen()]
                               ,strategy_facade=StrategyFacade())
            return unicorn
        if typ == "OTEFourH":
            gen_timeframes = self.generate_timeframes([240], [60])
            otefourh = OTEFourH(name="OTEFourH", timeframes=gen_timeframes, time_windows=[LondonOpen(), NYOpen()]
                                ,strategy_facade=StrategyFacade())
            return otefourh
        if typ == "LondonSB":
            gen_timeframes = self.generate_timeframes([240, 1], [60, 90])
            londonsb =  LondonSB(name="LondonSB", timeframes=gen_timeframes, time_windows=[SilverBulletLondon()]
                                 ,strategy_facade=StrategyFacade())
            return londonsb
        if typ == "DoubleFib":
            gen_timeframes = self.generate_timeframes([1], [90])
            time_windows:list[ITimeWindow] = [FirstQuarterWindow(), LastQuarterWindow()]
            doublefib =  DoubleFib(timeframes=gen_timeframes, time_windows=time_windows,strategy_facade=StrategyFacade())
            return doublefib
        logger.warning(f"No strategy found for {typ}")

    @staticmethod
    def generate_timeframes(timeframes: list[int], max_lens: list[int]) -> list[ExpectedTimeFrame]:
        gen_timeframes: list[ExpectedTimeFrame] = []
        for i in range(len(timeframes)):
            gen_timeframes.append(ExpectedTimeFrame(timeframe=timeframes[i], max_Len=max_lens[i]))
        return gen_timeframes

    @staticmethod
    def return_smt_strategy(typ: str, correlation: str, asset1: str, asset2: str) -> Strategy:
        if typ == "TestSMT":
            return TestSMTStrategy(_smt_handler=SMTHandler(asset_1=asset1, asset_2=asset2, correlation=correlation))
