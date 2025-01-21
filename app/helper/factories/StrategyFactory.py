from app.helper.strategy.FVGSession import FVGSession
from app.helper.strategy.Unicorn import Unicorn
from app.models.strategy.Strategy import Strategy
from app.monitoring.logging.logging_startup import logger


class StrategyFactory:
    @staticmethod
    def return_class(typ: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession()
        if typ == "Unicorn":
            return Unicorn()
        logger.debug(f"No strategy found for {typ}")
