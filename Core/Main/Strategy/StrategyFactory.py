from Core.Main.Strategy.Analyse.FVGSession import FVGSession
from Core.Main.Strategy.Analyse.Unicorn import Unicorn
from Core.Main.Strategy.Strategy import Strategy
from Interfaces.IFactory import IFactory


class StrategyFactory(IFactory):
    def returnClass(self, typ: str, subTyp: str, subTyp2: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(typ)
        if typ == "Unicorn":
            return Unicorn(typ)
