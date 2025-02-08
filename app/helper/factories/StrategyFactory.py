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
    @staticmethod
    def return_strategy(typ: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(name="FVGSession",timeframes=[ExpectedTimeFrame(timeframe=1,max_Len=90)])
        # todo
        if typ == "Unicorn":
            return Unicorn()
        if typ == "OTEFourH":
            return OTEFourH()
        if typ == "LondonSB":
            return LondonSB()
        if typ == "DoubleFib":
            return DoubleFib()
        logger.warning(f"No strategy found for {typ}")
    @staticmethod
    def return_smt_strategy(typ: str,correlation:str,asset1:str,asset2:str) -> Strategy:
        if typ == "TestSMT":
            return TestSMTStrategy(asset1,asset2,correlation)
