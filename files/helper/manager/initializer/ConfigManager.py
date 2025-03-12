import threading
from logging import Logger

from files.helper.factories.StrategyFactory import StrategyFactory
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.helper.manager.TradeManager import TradeManager
from files.models.asset.Relation import Relation
from files.models.asset.SMTPair import SMTPair
from files.monitoring.log_time import log_time


class ConfigManager:
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, trade_manager:TradeManager, asset_manager:AssetManager, relation_manager:RelationManager
                 , strategy_registry:StrategyRegistry,strategy_factory:StrategyFactory
                 , logger:Logger):

        self._trade_manager: TradeManager = trade_manager
        self._asset_manager: AssetManager = asset_manager
        self._relation_manager: RelationManager = relation_manager
        self._strategy_factory = strategy_factory
        self._strategy_manager: StrategyRegistry = strategy_registry
        self._logger: Logger = logger

    # endregion

    # region Starting Setup
    @log_time
    def initialize_managers(self):
        self._logger.info("Initializing ConfigManager")

        assets = self._asset_manager.return_assets()

        for asset in assets:
            self._asset_manager.register_asset(asset)

        relations = self._relation_manager.return_relations()

        smt_pairs = self._relation_manager.return_smt_pairs()

        for relation in relations:
            self._create_relation(relation=relation)

            for smt_pair in smt_pairs:
                self._create_smt(smt_pair=smt_pair,relation=relation)

        trades = self._trade_manager.get_trades()

        for trade in trades:
            self._trade_manager.register_trade(trade=trade)

        self._logger.info("ConfigManager initialized")
    # endregion

    def _create_relation(self, relation:Relation):
        try:
            self._asset_manager.add_relation(relation)

            strategy = self._strategy_factory.return_strategy(typ=relation.strategy)

            if strategy is None:
                return

            self._strategy_manager.register_strategy(relation=relation, strategy=strategy)
            self._logger.debug(f"Adding relation to asset:{relation.asset}")

            self._relation_manager.add_timeframes_to_asset(relation=relation)

        except Exception as e:
            self._logger.critical("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def _create_smt(self,smt_pair:SMTPair,relation:Relation):
        if ((relation.asset == smt_pair.asset_a or relation.asset == smt_pair.asset_b)
                and smt_pair.strategy == relation.strategy):
            strategy = self._strategy_factory.return_smt_strategy(typ=relation.strategy
                                                                  , correlation=smt_pair.correlation
                                                                  , asset2=smt_pair.asset_a
                                                                  , asset1=smt_pair.asset_b)
            if strategy is None:
                return

            asset_b = smt_pair.asset_b if relation.asset == smt_pair.asset_a else smt_pair.asset_a
            self._strategy_manager.register_smt_strategy(relation_smt=relation, strategy_smt=strategy,
                                                         asset2=asset_b)

            self._relation_manager.add_timeframes_to_asset(relation=relation)
