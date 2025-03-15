import threading
from logging import Logger

from files.db.mongodb.DataRepository import DataRepository
from files.helper.factories.StrategyFactory import StrategyFactory
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.helper.manager.TradeManager import TradeManager
from files.models.asset.Relation import Relation
from files.models.asset.SMTPair import SMTPair
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.monitoring.log_time import log_time

class RestartManager:
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(RestartManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, trade_manager:TradeManager, asset_manager:AssetManager, relation_manager:RelationManager
                 , strategy_registry:StrategyRegistry,strategy_factory:StrategyFactory,data_repository:DataRepository
                 , logger:Logger):

        self._trade_manager: TradeManager = trade_manager
        self._asset_manager: AssetManager = asset_manager
        self._data_repository: DataRepository = data_repository
        self._relation_manager: RelationManager = relation_manager
        self._strategy_factory = strategy_factory
        self._strategy_registry: StrategyRegistry = strategy_registry
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
            self._add_relation(relation=relation)

            for smt_pair in smt_pairs:
                self._create_smt(smt_pair=smt_pair,relation=relation)

            self._fill_strategy(relation=relation)

        trades = self._trade_manager.get_trades()

        for trade in trades:
            self._trade_manager.register_trade(trade=trade)

        self._logger.info("ConfigManager initialized")
    # endregion

    def _add_relation(self, relation:Relation):
        try:
            self._asset_manager.add_relation(relation)

            strategy = self._strategy_factory.return_strategy(typ=relation.strategy)

            if strategy is None:
                return

            self._strategy_registry.register_strategy(relation=relation, strategy=strategy)
            self._logger.debug(f"Adding relation to asset:{relation.asset}")

            self._relation_manager.add_timeframes_to_asset(relation=relation)
        except Exception as e:
            self._logger.critical("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def _fill_strategy(self, relation:Relation):
        expected_timeframes: list[ExpectedTimeFrame] = self._strategy_registry.return_expected_time_frame(
            relation=relation)

        for timeframe in expected_timeframes:
            timeframe: ExpectedTimeFrame = timeframe
            candles = self._data_repository.fetch_candles_by_asset_and_timeframe(asset=relation.asset,
                                                                                 timeframe=timeframe.timeframe,
                                                                                 lookback_candles=timeframe.max_Len)
            asset_class = self._asset_manager.return_asset_class(asset=relation.asset)
            if len(candles) >  1:
                section_size = 2  # Start mit 2 Kerzen (1,2)

                # Solange die Candles vorhanden sind und der Abschnittsindex in den verfügbaren Bereich passt
                while section_size <= len(candles):
                    # Nimm die ersten `section_size` Candles
                    section = candles[:section_size]

                    # Übergebe den Abschnitt an die Strategie-Registry
                    self._strategy_registry.get_entry(candles=section, relation=relation, timeFrame=timeframe.timeframe,asset_class=asset_class)

                    # Erhöhe den Abschnitts-Index um 2, also nächster Abschnitt hat 4 Kerzen, dann 6, usw.
                    section_size += 2

                # Falls du auch die restlichen Kerzen verarbeiten möchtest, falls sie nicht ganz in den Abschnitt passen
                if section_size > len(candles):
                    remaining_section = candles  # Falls der letzte Abschnitt weniger als der Abschnitts-Index ist
                    self._strategy_registry.get_entry(candles=remaining_section, relation=relation, timeFrame=timeframe.timeframe,asset_class=asset_class)

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
            self._strategy_registry.register_smt_strategy(relation_smt=relation, strategy_smt=strategy,
                                                          asset2=asset_b)

            self._relation_manager.add_timeframes_to_asset(relation=relation)