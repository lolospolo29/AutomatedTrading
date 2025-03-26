import threading

from logging import Logger

from files.db.repositories.StrategyRepository import StrategyRepository
from files.helper.builder.StrategyBuilder import StrategyBuilder
from files.models.strategy.EntryExitstrategy import EntryExitStrategy
from files.models.strategy.StrategyDTO import StrategyDTO
from files.models.strategy.EntryInput import EntryInput
from files.models.strategy.ExitInput import ExitInput
from files.models.strategy.Result import StrategyResult
from files.models.strategy.Strategy import Strategy

class StrategyManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(StrategyManager, cls).__new__(cls)
        return cls._instance

    def __init__(self,logger: Logger,strategy_repository: StrategyRepository,strategy_builder:StrategyBuilder):
        if not hasattr(self, "_initialized"):
            self.strategies: dict[str,Strategy] = {}
            self._strategy_repository:StrategyRepository = strategy_repository
            self._strategy_builder = strategy_builder
            self._logger = logger
            self._initialized = True

    def buildStrategy(self,strategy_dto:StrategyDTO):
        return (self._strategy_builder.create_strategy(strategy_dto.name).add_entry(strategy_dto.entry_strategy_id)
                .add_exit(strategy_dto.exit_strategy_id).build())

    def create_strategy(self, strategy_dto:StrategyDTO):
        self._strategy_repository.add_strategy(strategy_dto)
        strategy = self.buildStrategy(strategy_dto)
        self.add_strategy(strategy)

    def add_strategy(self, strategy:Strategy):
        with self._lock:
            if strategy.strategy_id not in self.strategies:
                self.strategies[strategy.strategy_id] = strategy
                self._logger.info(f"Strategy {strategy.name} registered for relation {strategy.strategy_id}")

    def get_strategies(self)->list[StrategyDTO]:
        return self._strategy_repository.find_strategies()

    def get_entry_exit_strategies(self)->list[EntryExitStrategy]:
        return self._strategy_repository.find_entry_exit_strategies()

    def get_entry(self, strategy_id:str, entry_input:EntryInput) -> StrategyResult:
        try:
            if strategy_id in self.strategies:
                return self.strategies[strategy_id].entry_strategy.get_entry(entry_input)
        except Exception as e:
            self._logger.exception(f"Get Entry Failed for {strategy_id}: {e}")

    def get_exit(self, strategy_id:str, exit_input:ExitInput) -> StrategyResult:
        try:
            if strategy_id in self.strategies:
                return self.strategies[strategy_id].exit_strategy(exit_input)
        except Exception as e:
            self._logger.exception(f"Get Exit Failed for {strategy_id}: {e}")

    def update_strategy(self, strategy_dto: StrategyDTO):
        with self._lock:
            if strategy_dto.strategy_id in self.strategies:
                self._strategy_repository.update_strategy(strategy_dto)

    def remove_strategy(self, strategy_dto:StrategyDTO):
        with self._lock:
            if strategy_dto.strategy_id in self.strategies:
                del self.strategies[strategy_dto.strategy_id]

    def delete_strategy(self, strategy_dto: StrategyDTO):
        with self._lock:
            if strategy_dto.strategy_id in self.strategies:
                del self.strategies[strategy_dto.strategy_id]
                self._strategy_repository.delete_strategy(strategy_dto)