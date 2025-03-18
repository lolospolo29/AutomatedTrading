from abc import abstractmethod, ABC

from files.models.strategy.ExitInput import ExitInput
from files.models.strategy.Result import StrategyResult

class ExitStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_exit(self, exit_input:ExitInput)->StrategyResult:
        pass