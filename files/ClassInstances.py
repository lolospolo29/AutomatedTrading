import logging
import queue
from functools import partial
from threading import Thread

from dotenv import load_dotenv
import os

from files.api.brokers.bybit.Bybit import Bybit
from files.api.brokers.bybit.BybitHandler import BybitHandler
from files.controller.AssetController import AssetController
from files.controller.RelationController import RelationController
from files.controller.SMTController import SMTController
from files.controller.ServiceController import ServiceController
from files.controller.StrategyController import StrategyController
from files.db.repositories.AssetRepository import AssetRepository
from files.db.repositories.BacktestRepository import BacktestRepository
from files.db.repositories.CandleRepository import CandleRepository
from files.db.repositories.NewsRepository import NewsRepository
from files.db.repositories.RelationRepository import RelationRepository
from files.db.repositories.SMTPairRepository import SMTPairRepository
from files.db.repositories.StrategyRepository import StrategyRepository
from files.db.repositories.TradeRepository import TradeRepository
from files.helper.builder.StrategyBuilder import StrategyBuilder
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.RiskManager import RiskManager
from files.helper.manager.SMTManager import SMTManager
from files.services.BrokerService import BrokerService
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.manager.StrategyManager import StrategyManager
from files.helper.mappers.ClassMapper import ClassMapper
from files.helper.functions.monitoring.logging.QueueHandler import QueueHandler
from files.helper.functions.monitoring.logging.TelegramLogHandler import TelegramLogHandler
from files.helper.functions.monitoring.monitorFolder import MonitorFolder
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

strategy_builder = StrategyBuilder()

# scrapper

economic_scrapper = EconomicScrapper(logger=logger)

# mapper

class_mapper = ClassMapper()

# broker

bybit = Bybit(api_key=os.getenv("BYBITKEY"),api_secret=os.getenv("BYBITSECRET"),uri=os.getenv("BYBITURL"))

bybit_handler = BybitHandler(logger=logger,bybit=bybit)

# DB
mongo_server = os.getenv("MONGODB")

trade_repository = TradeRepository(db_name="Trades",uri=mongo_server)

asset_repository = AssetRepository(db_name="TradingConfig",uri=mongo_server)

data_repository = CandleRepository(db_name="TradingData", uri=mongo_server)

relation_repository = RelationRepository(db_name="TradingConfig",uri=mongo_server)

news_repository = NewsRepository(db_name="News",uri=mongo_server)

backtest_repository = BacktestRepository(db_name="Backtest",uri=mongo_server)

strategy_repository = StrategyRepository(db_name="TradingConfig",uri=mongo_server)

smt_repository = SMTPairRepository(db_name="TradingConfig",uri=mongo_server)

# Registry 

broker_facade = BrokerRegistry()

broker_facade.register_handler(bybit_handler)

# Manager
risk_manager = RiskManager(logger=logger,max_risk_percentage=1,max_drawdown=4)

strategy_manager = StrategyManager(logger=logger,strategy_repository=strategy_repository,strategy_builder=strategy_builder)

asset_manager = AssetManager(asset_respository=asset_repository,trading_data_repository=data_repository,logger=logger)

smt_manager = SMTManager(smt_repository=smt_repository,logger=logger)

relation_manager = RelationManager(relation_repository=relation_repository, asset_manager=asset_manager,logger=logger)

trade_manager = BrokerService( broker_registry=broker_facade, logger=logger,)


# services

backtest_service = BacktestService(backtest_repository=backtest_repository, logger=logger, strategy_factory=strategy_builder)

news_service = NewsService(news_repository=news_repository,logger=logger,economic_scrapper=economic_scrapper)

telegram_service = TelegramService(token=os.getenv("TELEGRAMBOTTOKEN"), chat_id=os.getenv("TELEGRAMGROUPCHAT"),logger=logger)

trading_service = TradingService(asset_manager=asset_manager, trade_manager=trade_manager, strategy_registry=strategy_manager, news_service=news_service, telegram_service=telegram_service, logger=logger, asset_mapper=asset_mapper)

# Handler

new_file_handler = FileHandler(asset_manager=asset_manager, strategy_registry=strategy_manager, backtest_service=backtest_service, logger=logger)

# controller

asset_controller = AssetController(asset_manager=asset_manager,logger=logger)

relation_controller = RelationController(relation_manager=relation_manager,logger=logger)

service_controller = ServiceController(trading_service=trading_service, broker_service=trade_manager,  backtest_service=backtest_service,news_service=news_service,logger=logger)

strategy_controller = StrategyController(strategy_manager=strategy_manager,logger=logger)

smt_controller = SMTController(smt_manager=smt_manager,logger=logger)
# Logic

assets = asset_manager.get_assets()

for asset in assets:
    asset_manager.add_asset(asset)

relations = relation_manager.get_relations()

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