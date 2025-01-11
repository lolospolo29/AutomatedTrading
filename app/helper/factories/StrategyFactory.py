from app.helper.strategy.FVGSession import FVGSession
from app.helper.strategy.Unicorn import Unicorn
from app.models.strategy.Strategy import Strategy


class StrategyFactory:
    @staticmethod
    def returnClass(typ: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(typ)
        if typ == "Unicorn":
            return Unicorn(typ)
