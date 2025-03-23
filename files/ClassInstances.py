import logging
import queue
from functools import partial
from threading import Thread

from dotenv import load_dotenv
import os

from files.api.brokers.bybit.Bybit import Bybit
from files.api.brokers.bybit.BybitHandler import BybitHandler
from files.controller.AssetController import AssetController
from files.controller.SignalController import SignalController
from files.controller.StrategyController import StrategyController
from files.controller.ToolsController import ToolsController
from files.db.repositories.AssetRepository import AssetRepository
from files.db.repositories.BacktestRepository import BacktestRepository
from files.db.repositories.CandleRepository import CandleRepository
from files.db.repositories.NewsRepository import NewsRepository
from files.db.repositories.RelationRepository import RelationRepository
from files.db.repositories.StrategyRepository import StrategyRepository
from files.db.repositories.TradeRepository import TradeRepository
from files.helper.builder.StrategyBuilder import StrategyBuilder
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.RiskManager import RiskManager
from files.helper.manager.SMTManager import SMTManager
from files.helper.observer.MongoDBSyncObserver import MongoDBSyncObserver
from files.services.BrokerService import BrokerService
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.manager.StrategyManager import StrategyManager
from files.mappers.AssetMapper import AssetMapper
from files.mappers.BrokerMapper import BrokerMapper
from files.mappers.ClassMapper import ClassMapper
from files.mappers.DTOMapper import DTOMapper
from files.functions.monitoring.logging.QueueHandler import QueueHandler
from files.functions.monitoring.logging.TelegramLogHandler import TelegramLogHandler
from files.functions.monitoring.monitorFolder import MonitorFolder
from files.services.BacktestService import BacktestService
from tools.NewsService import NewsService
from tools.ScheduleService import ScheduleService
from tools.TelegramService import TelegramService
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

strategy_factory = StrategyBuilder()

if os.getenv("ENV") == "TST":
    watch_asset = MongoDBSyncObserver(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="Asset")
    watch_relation = MongoDBSyncObserver(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="Relation")
    watch_smt_pairs = MongoDBSyncObserver(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="SMTPairs")
    watch_strategy = MongoDBSyncObserver(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="Strategy")
    watch_exit_entry = MongoDBSyncObserver(client1_uri=os.getenv("MONGODBDEV"),client2_uri=os.getenv("MONGODB"),db_name="TradingConfig",collection_name="EntryExitStrategy")
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

trade_repository = TradeRepository(db_name="Trades",uri=mongo_server)

asset_repository = AssetRepository(db_name="TradingConfig",uri=mongo_server)

data_repository = CandleRepository(db_name="TradingData", uri=mongo_server)

relation_repository = RelationRepository(db_name="TradingConfig",uri=mongo_server)

news_repository = NewsRepository(db_name="News",uri=mongo_server)

backtest_repository = BacktestRepository(db_name="Backtest",uri=mongo_server)

strategy_repository = StrategyRepository(db_name="TradingConfig",uri=mongo_server)

# Registry 

broker_facade = BrokerRegistry()

broker_facade.register_handler(bybit_handler)


# Manager
risk_manager = RiskManager(logger=logger,max_risk_percentage=1,max_drawdown=4)

strategy_manager = StrategyManager(logger=logger,strategy_repository=strategy_repository)

asset_manager = AssetManager(asset_respository=asset_repository,trading_data_repository=data_repository,logger=logger)

smt_manager = SMTManager(logger=logger,relation_repository=relation_repository,asset_repository=asset_repository,asset_manager=asset_manager)

relation_manager = RelationManager(relation_repository=relation_repository, asset_manager=asset_manager, strategy_registry=strategy_manager, logger=logger,
                                   strategy_builder=strategy_factory,strategy_repository=strategy_repository)

trade_manager = BrokerService(trade_repository=trade_repository, broker_facade=broker_facade, risk_manager=risk_manager, relation_manager=relation_manager, logger=logger, broker_mapper=broker_mapper, class_mapper=class_mapper)


# services

backtest_service = BacktestService(backtest_repository=backtest_repository,logger=logger,strategy_factory=strategy_factory)

news_service = NewsService(news_repository=news_repository,logger=logger,economic_scrapper=economic_scrapper)

telegram_service = TelegramService(token=os.getenv("TELEGRAMBOTTOKEN"), chat_id=os.getenv("TELEGRAMGROUPCHAT"),logger=logger)

trading_service = TradingService(asset_manager=asset_manager, trade_manager=trade_manager, strategy_registry=strategy_manager, news_service=news_service, telegram_service=telegram_service, logger=logger, asset_mapper=asset_mapper)

# Handler

new_file_handler = FileHandler(asset_manager=asset_manager, strategy_registry=strategy_manager, backtest_service=backtest_service, logger=logger)

# controller

signal_controller = SignalController(trading_service=trading_service, broker_service=trade_manager, relation_manager=relation_manager, smt_manager=smt_manager,logger=logger)

asset_controller = AssetController(asset_manager=asset_manager,logger=logger)

strategy_controller = StrategyController(strategy_manager=strategy_manager,logger=logger)

tools_controller = ToolsController(logger=logger,news_service=news_service,backtest_service=backtest_service)

# Logic

assets = asset_manager.return_assets()

for asset in assets:
    asset_manager.add_asset(asset)

relations = relation_manager.return_relations()

smt_pairs = smt_manager.return_smt_pairs()

for relation in relations:
    relation_manager.add_relation(relation=relation)

for smt_pair in smt_pairs:
    smt_manager.add_smt(smt_pair)

trades = trade_manager.get_trades()

for trade in trades:
    trade_manager.register_trade(trade=trade)

schedule_manager = ScheduleService(logger=logger)

schedule_manager.every_day_add_schedule("News","12:00",news_service.run_news_scheduler)

news_service.fetch_news()

thread = Thread(target=partial(MonitorFolder, new_file_handler, "incomingFiles"))
thread.start()