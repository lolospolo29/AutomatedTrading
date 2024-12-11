from Core.Main.Strategies.Analyse.FVGSession import FVGSession
from Core.Main.Strategies.Strategy import Strategy
from Interfaces.IFactory import IFactory


class StrategyFactory(IFactory):
    def returnClass(self, typ: str, subTyp: str, subTyp2: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(typ)
