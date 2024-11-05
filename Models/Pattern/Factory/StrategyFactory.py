from Interfaces.IFactory import IFactory
from Models.Main.Strategies.Entry.FVGEntry import FVGEntry
from Models.Main.Strategies.Exit.FVGExit import FVGExit
from Models.Main.Strategies.ExitEntryStrategy import ExitEntryStrategy
from Models.Main.Strategies.Strategy import Strategy
from Models.Main.Strategies.StrategyAnalyse.FVGSession import FVGSession


class StrategyFactory(IFactory):
    def returnClass(self, typ: str, subTyp: str, subTyp2: str) -> Strategy:

        entry = self.returnSubTyp(subTyp)

        exit = self.returnSubTyp2(subTyp2)

        if typ == "FVGSession":
            FVGSession(typ,entry,exit)

    @staticmethod
    def returnSubTyp(subTyp: str) -> ExitEntryStrategy:
        if subTyp == "FVGEntry":
            return FVGEntry(subTyp)

    @staticmethod
    def returnSubTyp2(subTyp2: str):
        if subTyp2 == "FVGExit":
            return FVGExit(subTyp2)
