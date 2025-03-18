from files.models.strategy.EntryStrategy import EntryStrategy
from files.models.strategy.ExitStrategy import ExitStrategy
from files.models.strategy.Strategy import Strategy


class SwingWeekly(Strategy):
    def __init__(self, entryStrategy: EntryStrategy, exitStrategy: ExitStrategy):
        self.entryStrategy = entryStrategy
        self.exitStrategy = exitStrategy

    @property
    def exit_strategy(self) -> ExitStrategy:
        return self.exitStrategy

    @property
    def entry_strategy(self) -> EntryStrategy:
        return self.entryStrategy

    @property
    def name(self) -> str:
        return self.name