from app.helper.strategy.FVGSession import FVGSession
from app.helper.strategy.Unicorn import Unicorn
from app.models.strategy.Strategy import Strategy


class StrategyFactory:
    @staticmethod
    def return_class(typ: str) -> Strategy:

        if typ == "FVG":
            return FVGSession()
        if typ == "Unicorn":
            return Unicorn()
