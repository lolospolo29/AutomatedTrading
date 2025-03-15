import logging
import queue
from functools import partial
from threading import Thread

from dotenv import load_dotenv
import os

from files.api.brokers.bybit.Bybit import Bybit
from files.api.brokers.bybit.BybitHandler import BybitHandler
from files.controller.SignalController import SignalController
from files.db.mongodb.AssetRepository import AssetRepository
from files.db.mongodb.BacktestRepository import BacktestRepository
from files.db.mongodb.DataRepository import DataRepository
from files.db.mongodb.NewsRepository import NewsRepository
from files.db.mongodb.RelationRepository import RelationRepository
from files.db.mongodb.TradeRepository import TradeRepository
from files.helper.factories.MongoDBSyncFactory import MongoDBSyncFactory
from files.helper.factories.StrategyFactory import StrategyFactory
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.RiskManager import RiskManager
from files.helper.manager.TradeManager import TradeManager
from files.helper.manager.RestartManager import RestartManager
from files.helper.observer.MongoDBSyncObserver import MongoDBSyncObserver
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.mappers.AssetMapper import AssetMapper
from files.mappers.BrokerMapper import BrokerMapper
from files.mappers.ClassMapper import ClassMapper
from files.mappers.DTOMapper import DTOMapper
from files.monitoring.logging.QueueHandler import QueueHandler
from files.monitoring.logging.TelegramLogHandler import TelegramLogHandler
from files.monitoring.monitorFolder import MonitorFolder
from files.services.BacktestService import BacktestService
from files.services.NewsService import NewsService
from files.services.ScheduleService import ScheduleService
from files.services.TelegramService import TelegramService
from files.services.TradingService import TradingService
from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.FileHandler import FileHandler

load_dotenv()

# Secret Manager
# Logging
log_queue = queue.Queue()
logger = logging.getLogger()

queue_handler = QueueHandler(log_queue)
telegram_handler = TelegramLogHandler(token=os.getenv("TELEGRAMBOTTOKEN"),chat_id=os.getenv("TELEGRAMCHAT"))

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Set global logging level (should be the lowest level needed)
logger.setLevel(logging.DEBUG)  # Capture all levels

# Configure Queue Handler (Logs everything, including DEBUG)
queue_handler.setLevel(logging.INFO)
queue_handler.setFormatter(formatter)
logger.addHandler(queue_handler)

# Configure Telegram Handler (Only logs ERROR and above)
telegram_handler.setLevel(logging.ERROR)
telegram_handler.setFormatter(formatter)
logger.addHandler(telegram_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
# Add CSVFileHandler to write logs to a CSV file
#csv_handler = CSVFileHandler('logs.csv')
#csv_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
#logger.addHandler(csv_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
#sys.stdout = StreamToLogger(logger, logging.INFO)
#sys.stderr = StreamToLogger(logger, logging.ERROR)

# factory

strategy_factory = StrategyFactory()

if os.getenv("ENV") == "TST":
    sync_factory = MongoDBSyncFactory()
    watch_asset = sync_factory.create_sync_watcher(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="Asset")
    watch_relation = sync_factory.create_sync_watcher(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="Relation")
    watch_smt_pairs = sync_factory.create_sync_watcher(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="SMTPairs")
# scrapper

economic_scrapper = EconomicScrapper(logger=logger)

# mapper

dto_mapper = DTOMapper()
asset_mapper = AssetMapper()
class_mapper = ClassMapper()
broker_mapper = BrokerMapper()

# broker

bybit = Bybit(api_key=os.getenv("BYBITKEY"),api_secret=os.getenv("BYBITSECRET"),uri=os.getenv("BYBITURL"))

bybit_handler = BybitHandler(logger=logger, class_mapper=class_mapper,bybit=bybit)

# DB
mongo_server = os.getenv("MONGODB")

trade_repository = TradeRepository(db_name="Trades",uri=mongo_server,logger=logger,dto_mapper=dto_mapper)

asset_repository = AssetRepository(db_name="TradingConfig",uri=mongo_server,dto_mapper=dto_mapper)

data_repository = DataRepository(db_name="TradingData",uri=mongo_server,dto_mapper=dto_mapper)

relation_repository = RelationRepository(db_name="TradingConfig",uri=mongo_server,dto_mapper=dto_mapper)

news_repository = NewsRepository(db_name="News",uri=mongo_server,dto_mapper=dto_mapper)

backtest_repository = BacktestRepository(db_name="Backtest",uri=mongo_server,dto_mapper=dto_mapper)

# Registry 

strategy_registry = StrategyRegistry(logger=logger)
broker_facade = BrokerRegistry()

broker_facade.register_handler(bybit_handler)

risk_manager = RiskManager()

# Manager

asset_manager = AssetManager(asset_respository=asset_repository,trading_data_repository=data_repository,logger=logger)

relation_manager = RelationManager(relation_repository=relation_repository,asset_manager=asset_manager,asset_repository=asset_repository,strategy_registry=strategy_registry,logger=logger,strategy_factory=strategy_factory)

trade_manager = TradeManager(trade_repository=trade_repository,broker_facade=broker_facade,risk_manager=risk_manager,relation_manager=relation_manager, logger=logger,broker_mapper=broker_mapper,class_mapper=class_mapper)

config_manager = RestartManager(trade_manager=trade_manager, asset_manager=asset_manager, relation_manager=relation_manager,
                                strategy_registry=strategy_registry, logger=logger, strategy_factory=strategy_factory, data_repository=data_repository)

# services

backtest_service = BacktestService(backtest_repository=backtest_repository,logger=logger,strategy_factory=strategy_factory)

news_service = NewsService(news_repository=news_repository,logger=logger,economic_scrapper=economic_scrapper)

telegram_service = TelegramService(token=os.getenv("TELEGRAMBOTTOKEN"), chat_id=os.getenv("TELEGRAMGROUPCHAT"),logger=logger)

trading_service = TradingService(asset_manager=asset_manager, trade_manager=trade_manager, strategy_registry=strategy_registry, news_service=news_service, telegram_service=telegram_service, logger=logger,asset_mapper=asset_mapper)

# Handler

new_file_handler = FileHandler(asset_manager=asset_manager, strategy_registry=strategy_registry, backtest_service=backtest_service, logger=logger)

# controller

signal_controller = SignalController(trading_service=trading_service, news_service=news_service,asset_manager=asset_manager, trade_manager=trade_manager,relation_manager=relation_manager,backtest_service=backtest_service,logger=logger,strategy_registry=strategy_registry)

# Logic

config_manager.initialize_managers()

schedule_manager = ScheduleService(logger=logger)

schedule_manager.every_day_add_schedule("News","12:00",news_service.run_news_scheduler)

news_service.fetch_news()

thread = Thread(target=partial(MonitorFolder, new_file_handler, "incomingFiles"))
thread.start()