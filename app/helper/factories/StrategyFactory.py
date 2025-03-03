from app.helper.template.time.London import LondonOpen
from app.helper.template.time.NYOpen import NYOpen
from app.helper.template.time.macro.silverBullet.SilverBulletLondon import SilverBulletLondon
from app.helper.facade.StrategyFacade import StrategyFacade
from app.helper.strategy.DoubleFib import DoubleFib
from app.helper.strategy.FVGSession import FVGSession
from app.helper.strategy.LondonSB import LondonSB
from app.helper.strategy.OTEFourH import OTEFourH
from app.helper.strategy.TestSMT import TestSMTStrategy
from app.helper.strategy.Unicorn import Unicorn
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.monitoring.logging.logging_startup import logger


class StrategyFactory:
    def return_strategy(self, typ: str) -> Strategy:
        if typ == "FVGSession":
            fvg =  FVGSession(name=typ, timeframes=[ExpectedTimeFrame(timeframe=1, max_Len=90)]
                              ,strategy_facade=StrategyFacade())
            return fvg
        if typ == "Unicorn":
            gen_timeframes = self._generate_timeframes([240, 5], [1, 90])
            unicorn =  Unicorn(name="Unicorn", timeframes=gen_timeframes, time_windows=[LondonOpen(), NYOpen()]
                               ,strategy_facade=StrategyFacade())
            return unicorn
        if typ == "OTEFourH":
            gen_timeframes = self._generate_timeframes([240], [60])
            otefourh = OTEFourH(name=typ, timeframes=gen_timeframes, time_windows=[LondonOpen(), NYOpen()]
                                ,strategy_facade=StrategyFacade())
            return otefourh
        if typ == "LondonSB":
            gen_timeframes = self._generate_timeframes([240, 1], [60, 90])
            londonsb =  LondonSB(name=typ, timeframes=gen_timeframes, time_windows=[SilverBulletLondon()]
                                 ,strategy_facade=StrategyFacade())
            return londonsb
        if typ == "DoubleFib":
            gen_timeframes = self._generate_timeframes([1], [240])
            doublefib =  DoubleFib(name=typ,timeframes=gen_timeframes, time_windows=[NYOpen()],strategy_facade=StrategyFacade())
            return doublefib
        logger.warning(f"No strategy found for {typ}")

    @staticmethod
    def _generate_timeframes(timeframes: list[int], max_lens: list[int]) -> list[ExpectedTimeFrame]:
        gen_timeframes: list[ExpectedTimeFrame] = []
        for i in range(len(timeframes)):
            gen_timeframes.append(ExpectedTimeFrame(timeframe=timeframes[i], max_Len=max_lens[i]))
        return gen_timeframes

    @staticmethod
    def return_smt_strategy(typ: str, correlation: str, asset1: str, asset2: str) -> Strategy:
        if typ == "TestSMT":
            return TestSMTStrategy()
