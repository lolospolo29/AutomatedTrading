from app.strategy.FVGSession import FVGSession
from app.strategy.Unicorn import Unicorn
from app.models.strategy.Strategy import Strategy


class StrategyFactory:
    @staticmethod
    def returnClass(typ: str, subTyp: str, subTyp2: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(typ)
        if typ == "Unicorn":
            return Unicorn(typ)
