from abc import abstractmethod, ABC

from files.models.strategy import ExitStrategy
from files.models.strategy.EntryStrategy import EntryStrategy


class Strategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Jede Strategie muss einen Namen haben"""
        pass

    @property
    @abstractmethod
    def entry_strategy(self) -> EntryStrategy:
        """Getter für Entry-Strategie"""
        pass

    @entry_strategy.setter
    @abstractmethod
    def entry_strategy(self, entry_strategy: EntryStrategy):
        """Setter für Entry-Strategie"""
        pass

    @property
    @abstractmethod
    def exit_strategy(self) -> ExitStrategy:
        """Getter für Exit-Strategie"""
        pass

    @exit_strategy.setter
    @abstractmethod
    def exit_strategy(self, exit_strategy: ExitStrategy):
        """Setter für Exit-Strategie"""
        pass