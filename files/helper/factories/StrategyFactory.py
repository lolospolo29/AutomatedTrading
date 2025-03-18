from files.helper.strategy.entry.DoubleFib15 import DoubleFib15
from files.helper.strategy.entry.DoubleFib1 import DoubleFib1
from files.helper.strategy.entry.DoubleFib5 import DoubleFib5
from files.helper.strategy.entry.SB import LondonSB
from files.models.strategy.Strategy import Strategy


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