import uuid

from files.models.strategy.ExitStrategy import ExitStrategy
from files.models.strategy.EntryStrategy import EntryStrategy

class Strategy:

    def __init__(self, name,id:str=None):
        self._name = name
        if id is None:
           id =  str(uuid.uuid4())
        self._strategy_id = id
        self.entry_strategy = None
        self.exitStrategy = None

    @property
    def strategy_id(self):
        return self._strategy_id

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