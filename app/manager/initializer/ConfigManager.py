import threading

from app.db.mongodb.MongoDBConfig import MongoDBConfig
from app.db.mongodb.MongoDBTrades import MongoDBTrades
from app.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.helper.factories.StrategyFactory import StrategyFactory
from app.helper.registry.SemaphoreRegistry import SemaphoreRegistry
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.asset.Relation import Relation
from app.monitoring.log_time import log_time
from app.monitoring.logging.logging_startup import logger


class ConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing
    def __init__(self):

        self._mongo_db_config: MongoDBConfig = MongoDBConfig()
        self._mongo_db_trades: MongoDBTrades = MongoDBTrades()
        self._trade_manager: TradeManager = TradeManager()
        self._trade_semaphore_registry: SemaphoreRegistry = SemaphoreRegistry()
        self._asset_manager: AssetManager = AssetManager()
        self._strategy_manager: StrategyManager = StrategyManager()
        self._strategy_factory: StrategyFactory = StrategyFactory()

    # endregion

    # region Starting Setup
    @log_time
    def run_starting_setup(self):
        logger.info("Initializing ConfigManager")

        assets_db: list = self._mongo_db_config.load_data("Asset", None)
        asset_dict: dict = {}
        for asset_db in assets_db:
            dto:AssetDTO = AssetDTO(**asset_db)

            query = self._mongo_db_config.buildQuery("id", dto.assetClass)
            asset_class_db: list = self._mongo_db_config.load_data("AssetClasses", query)
            asset_class :AssetClassDTO= AssetClassDTO(**asset_class_db[0])

            query = self._mongo_db_config.buildQuery("assetId", dto.assetClass)
            relations_db: list = self._mongo_db_config.load_data("Relation", query)

            for relation_db in relations_db:
                relation :RelationDTO = RelationDTO(**relation_db)

                query = self._mongo_db_config.buildQuery("brokerId", relation.brokerId)
                brokers: list = self._mongo_db_config.load_data("Broker", query)

                query = self._mongo_db_config.buildQuery("strategyId", relation.brokerId)
                strategies: list = self._mongo_db_config.load_data("Broker", query)

                broker:BrokerDTO = BrokerDTO(**brokers[0])
                strategy_dto:StrategyDTO = StrategyDTO(**strategies[0])

                strategy = self._strategy_factory.return_strategy(strategy_dto.name)

                Relation(asset=dto.name,strategy=strategy_dto.name,broker=broker.name,max_trades=relation.maxTrades)



        smtPairs: list = self._mongo_db_config.load_data("SMTPairs", None)

        trades: list = self._mongo_db_trades.find_trade_or_trades_by_id()

        # todo

    # endregion
