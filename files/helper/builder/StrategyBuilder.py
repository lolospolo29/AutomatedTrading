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