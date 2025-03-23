import threading

from logging import Logger

from files.db.repositories.StrategyRepository import StrategyRepository
from files.models.strategy.EntryExitstrategyDTO import EntryExitStrategyDTO
from files.models.strategy.StrategyDTO import StrategyDTO
from files.models.asset.Relation import Relation
from files.models.strategy.EntryInput import EntryInput
from files.models.strategy.ExitInput import ExitInput
from files.models.strategy.Result import StrategyResult
from files.models.strategy.Strategy import Strategy

class StrategyManager:
    """
    Manages strategy instances for asset-broker relations.

    StrategyManager provides a singleton implementation to manage and interact
    with trading strategies associated with specific asset-broker relations.
    It offers methods to register new strategies and retrieve expected insights
    or actions (e.g., entry or exit strategies) based on provided data.

    :ivar strategies: Dictionary mapping AssetBrokerStrategyRelation instances
                      to their associated Strategy instances.
    :type strategies: dict[Relation, Strategy]
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(StrategyManager, cls).__new__(cls)
        return cls._instance

    # region Initializing

    def __init__(self,logger: Logger,strategy_repository: StrategyRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.strategies: dict[Relation,Strategy] = {}
            self._logger = logger
            self._strategy_repository:StrategyRepository = strategy_repository
            self._initialized = True  # Markiere als initialisiert

    # endregion
    def register_smt_strategy(self, relation_smt:Relation, strategy_smt:Strategy, asset2:str) -> bool:
        if relation_smt not in self.strategies:
            for relation, strategy in self.strategies.items():  # Iteriere durch Relation-Struktur und Strategien
                if relation.asset == asset2:  # Prüfe, ob die Relation das gewünschte Asset enthält
                    self.strategies[relation_smt] = strategy
                    return True
            self.strategies[relation_smt] = strategy_smt
            self._logger.info(f"Strategy {strategy_smt.name} registered for relation {relation_smt}")
            return True
        else:
            self._logger.info(f"Strategy {strategy_smt.name} already registered")
            return False

    def register_strategy(self, relation:Relation, strategy:Strategy) -> bool:
        if relation not in self.strategies:
            self.strategies[relation] = strategy
            self._logger.info(f"Strategy {strategy.name} registered for relation {relation}")
            return True
        else:
            self._logger.info(f"Strategy {strategy.name} already registered")
            return False

    def update_relation(self, relation:Relation):
            for relation_, strategy in self.strategies.items():
                if relation_.id == relation.id:
                    self.delete_relation(relation_)
                    self.register_strategy(relation,strategy)
                    self._logger.info(f"Strategy {relation_.asset} updated")
                    return
                    # update the relation not strategy with the input relation

    def delete_relation(self, relation:Relation):
        try:
            if relation in self.strategies:
                del self.strategies[relation]
                self._logger.info(f"Strategy {relation.asset} deleted")
        except Exception as e:
            self._logger.exception("Failed to delete strategy {strategy},Error:{e}".format(strategy=relation, e=e))

    def get_entry(self, relation:Relation, entry_input:EntryInput) -> StrategyResult:
        try:
            if entry_input in self.strategies:
                self._logger.info(f"Strategy {relation.asset} get Entry")
                return self.strategies[relation].entry_strategy.get_entry(entry_input)
        except Exception as e:
            self._logger.exception(f"Get Entry Failed for {relation.strategy}/{relation.asset}: {e}")

    def get_exit(self, relation:Relation, exit_input:ExitInput) -> StrategyResult:
        try:
            if relation in self.strategies:
                return self.strategies[relation].exit_strategy(exit_input)
        except Exception as e:
            self._logger.exception(f"Get Exit Failed for {relation.strategy}/{relation}: {e}")

    # region CRUD

    def create_strategy(self, strategy_dto:StrategyDTO):
        self._strategy_repository.add_strategy(strategy_dto)

    def find_strategies(self)->list[StrategyDTO]:
        return self._strategy_repository.find_strategies()

    def find_entry_exit_strategies(self)->list[EntryExitStrategyDTO]:
        return self._strategy_repository.find_entry_exit_strategies()

    def update_strategy(self,strategy_dto:StrategyDTO):
        self._strategy_repository.update_relation(strategy_dto)

    def delete_strategy(self,strategy_dto:StrategyDTO):
        self._strategy_repository.delete_strategy(strategy_dto)