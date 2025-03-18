from abc import abstractmethod, ABC

from files.models.strategy import EntryInput
from files.models.strategy.Result import StrategyResult

class EntryStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_entry(self, entryInput:EntryInput)->StrategyResult:
        pass