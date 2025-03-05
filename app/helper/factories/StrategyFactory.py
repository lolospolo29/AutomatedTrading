from app.helper.strategy.DoubleFib import DoubleFib
from app.helper.strategy.SB import LondonSB
from app.models.strategy.Strategy import Strategy
from app.monitoring.logging.logging_startup import logger


class StrategyFactory:
    @staticmethod
    def return_strategy(typ: str) -> Strategy:
        if typ == "LondonSB":
            londonsb =  LondonSB()
            return londonsb
        if typ == "DoubleFib":
            doublefib =  DoubleFib()
            return doublefib
        logger.warning(f"No strategy found for {typ}")

    @staticmethod
    def return_smt_strategy(typ: str, correlation: str, asset1: str, asset2: str) -> Strategy:
        pass
