from files.helper.strategy.entry.DoubleFib15 import DoubleFib15
from files.helper.strategy.entry.DoubleFib1 import DoubleFib1
from files.helper.strategy.entry.DoubleFib5 import DoubleFib5
from files.helper.strategy.entry.SB import LondonSB
from files.models.strategy.ExitStrategy import ExitStrategy
from files.models.strategy.Strategy import Strategy


class StrategyBuilder:
    def __init__(self):
        self._strategy = None

    def create_strategy(self,name: str):
        self._strategy = Strategy(name=name)
        return self

    def add_entry(self, typ: str):
        return self

    def add_exit(self, typ: str):
        return self

    def build(self):
        return self._strategy