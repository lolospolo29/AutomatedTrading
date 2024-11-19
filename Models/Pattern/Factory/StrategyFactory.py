from Interfaces.IFactory import IFactory
from Models.Main.Strategies.Analyse.FVGSession import FVGSession
from Models.Main.Strategies.Strategy import Strategy


class StrategyFactory(IFactory):
    def returnClass(self, typ: str, subTyp: str, subTyp2: str) -> Strategy:

        if typ == "FVGSession":
            return FVGSession(typ)
