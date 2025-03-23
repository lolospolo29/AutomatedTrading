from files.models.strategy import ExitStrategy
from files.models.strategy.EntryStrategy import EntryStrategy

class Strategy:

    def __init__(self, name):
        self._name = name
        self.entry_strategy = None
        self.exitStrategy = None

    @property
    def name(self) -> str:
        """Jede Strategie muss einen Namen haben"""
        return self._name

    @property
    def entry_strategy(self) -> EntryStrategy:
        """Getter für Entry-Strategie"""
        return self.entry_strategy

    @entry_strategy.setter
    def entry_strategy(self, entry_strategy: EntryStrategy):
        """Setter für Entry-Strategie"""
        self.entry_strategy = entry_strategy

    @property
    def exit_strategy(self) -> ExitStrategy:
        """Getter für Exit-Strategie"""
        return self.exit_strategy

    @exit_strategy.setter
    def exit_strategy(self, exit_strategy: ExitStrategy):
        """Setter für Exit-Strategie"""
        self.exit_strategy = exit_strategy