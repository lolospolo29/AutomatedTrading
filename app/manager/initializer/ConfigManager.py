import threading

from app.db.mongodb.MongoDBConfig import MongoDBConfig
from app.db.mongodb.MongoDBTrades import MongoDBTrades
from app.helper.factories.StrategyFactory import StrategyFactory
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
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
        self._trade_semaphore_registry: TradeSemaphoreRegistry = TradeSemaphoreRegistry()
        self._asset_manager: AssetManager = AssetManager()
        self._strategy_manager: StrategyManager = StrategyManager()
        self._strategy_factory: StrategyFactory = StrategyFactory()

    # endregion

    # region Starting Setup
    @log_time
    def run_starting_setup(self):
        logger.info("Initializing ConfigManager")

        assets: list = self._mongo_db_config.load_data("Asset", None)

        brokers: list = self._mongo_db_config.load_data("Broker", None)
        strategies: list = self._mongo_db_config.load_data("Strategy", None)
        relations: list = self._mongo_db_config.load_data("AssetBrokerStrategyRelation"
                                                          , None)
        smtPairs: list = self._mongo_db_config.load_data("SMTPairs", None)
        asset_classes: list = self._mongo_db_config.load_data("AssetClasses", None)

        trades: list = self._mongo_db_trades.find_trade_or_trades_by_id()

        # todo


    # endregion
