from files.helper.strategy.DoubleFib15 import DoubleFib15
from files.helper.strategy.DoubleFib1 import DoubleFib1
from files.helper.strategy.DoubleFib5 import DoubleFib5
from files.helper.strategy.SB import LondonSB
from files.models.strategy.Strategy import Strategy
from files.monitoring.logging.logging_startup import logger


class StrategyFactory:
    @staticmethod
    def return_strategy(typ: str) -> Strategy:
        if typ == "LondonSB":
            londonsb =  LondonSB()
            return londonsb
        if typ == "DoubleFib15":
            doublefib =  DoubleFib15()
            return doublefib
        if typ == "DoubleFib1":
            doublefib =  DoubleFib1()
            return doublefib
        if typ == "DoubleFib5":
            doublefib =  DoubleFib5()
            return doublefib
        logger.warning(f"No strategy found for {typ}")

    @staticmethod
    def return_smt_strategy(typ: str, correlation: str, asset1: str, asset2: str) -> Strategy:
        pass
