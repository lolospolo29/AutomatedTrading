import threading

from logging import Logger

from files.db.repositories.RelationRepository import RelationRepository
from files.db.repositories.StrategyRepository import StrategyRepository
from files.models.asset.Category import Category
from files.models.strategy.EntryExitstrategyDTO import EntryExitStrategyDTO
from files.models.strategy.StrategyDTO import StrategyDTO
from files.helper.builder.StrategyBuilder import StrategyBuilder
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.StrategyManager import StrategyManager
from files.models.asset.Relation import Relation
from files.models.strategy.Strategy import Strategy


class RelationManager:
    """
    Manages relationships between assets, strategies, and timeframes by coordinating
    with the repository, asset manager, and strategy manager. Provides functionality
    to create relations and append timeframes to assets.

    This singleton class ensures a centralized management of asset relationships
    and expected timeframes by using threading for safe instantiation. It aligns
    different components by interacting with asset data and strategies.

    """
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(RelationManager, cls).__new__(cls)
        return cls._instance


    def __init__(self, relation_repository:RelationRepository
                 , asset_manager:AssetManager, strategy_repository:StrategyRepository
                 , logger:Logger, strategy_registry:StrategyManager
                 , strategy_builder:StrategyBuilder):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._relation_repository = relation_repository
            self._strategy_repository = strategy_repository
            self._asset_manager = asset_manager
            self._strategy_manager = strategy_registry
            self._strategy_builder = strategy_builder
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    def add_relation(self, relation:Relation):
        self._asset_manager.add_relation(relation)
        strategy_dto:StrategyDTO = self._strategy_repository.find_strategy_by_name(relation.strategy_name)
        entry:EntryExitStrategyDTO = self._strategy_repository.find_entry_exit_strategy_by_id(strategy_dto.entry_strategy_id)
        exit:EntryExitStrategyDTO = self._strategy_repository.find_entry_exit_strategy_by_id(strategy_dto.exit_strategy_id)
        strategy:Strategy = self._strategy_builder.create_strategy(relation.strategy).add_entry(entry.name).add_exit(exit.name).build()

        self._strategy_manager.register_strategy(relation=relation,strategy=strategy)

    def create_relation(self, relation:Relation):
        try:
            self._relation_repository.add_relation(relation)
            self.add_relation(relation)

            self._logger.debug(f"Adding relation to asset:{relation.asset}")
            self._logger.debug(f"Adding relation to db:{relation}")

        except Exception as e:
            self._logger.critical("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def return_strategies(self)->list[str]:
        strategies:list[StrategyDTO] =  self._relation_repository.find_strategies()
        names = []

        for strategy in strategies:
            strategy:StrategyDTO
            names.append(strategy.name)
        return names

    def return_relation_for_id(self,relation_id:int)->Relation:
        relation_dto:Relation = self._relation_repository.find_relation_by_id(relation_id)

        asset_dto = self._relation_repository.find_asset_by_id(relation_dto.asset_id)
        broker_dto = self._relation_repository.find_broker_by_id(relation_dto.broker_id)
        strategy_dto = self._relation_repository.find_strategy_by_id(relation_dto.strategy_id)
        category_dto = self._relation_repository.find_category_by_id(relation_dto.category_id)

        relation = Relation(asset=asset_dto.name, broker=broker_dto.name, strategy=strategy_dto.name
                            , max_trades=relation_dto.max_trades, id=relation_dto.relation_id, category=category_dto.name)
        return relation

    def return_relations(self)->list[Relation]:
        relation_dtos:list[Relation] = self._relation_repository.find_relations()

        relations:list[Relation] = []
        for relation_dto in relation_dtos:
            relations.append(self.return_relation_for_id(relation_dto.relation_id))
        return relations

    def update_relation(self, relation:Relation):
        self._asset_manager.update_relation(relation=relation)
        self._strategy_manager.update_relation(relation=relation)
        self._relation_repository.update_relation(relation=relation)

    def delete_relation(self, relation:Relation):
        self._asset_manager.remove_relation(relation=relation)
        self._strategy_manager.delete_relation(relation=relation)
        self._relation_repository.delete_relation(relation=relation)

    def return_categories(self)->list[Category]:
        return self._relation_repository.find_categories()