import time
from functools import partial
from threading import Thread

from dotenv import load_dotenv
from watchdog.observers import Observer

from files.api.brokers.bybit.BybitHandler import BybitHandler
from files.controller.SignalController import SignalController
from files.db.mongodb.AssetRepository import AssetRepository
from files.db.mongodb.BacktestRepository import BacktestRepository
from files.db.mongodb.NewsRepository import NewsRepository
from files.db.mongodb.RelationRepository import RelationRepository
from files.db.mongodb.TradeRepository import TradeRepository
from files.helper.registry.BrokerRegistry import BrokerRegistry
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.RiskManager import RiskManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.helper.manager.TradeManager import TradeManager
from files.helper.manager.initializer.SecretsManager import SecretsManager
from files.services.BacktestService import BacktestService
from files.services.NewsService import NewsService
from files.services.ScheduleService import ScheduleService
from files.services.TradingService import TradingService
from tools.FileHandler import FileHandler
from files.helper.manager.initializer.ConfigManager import ConfigManager

# Broker

load_dotenv()


secret_manager = SecretsManager()

bybit = BybitHandler()

broker_facade = BrokerRegistry()
broker_facade.register_handler("Bybit", bybit)

risk_manager = RiskManager()

# DB

mongo_server = secret_manager.return_secret("mongodb")

trade_repository = TradeRepository(db_name="Trades",uri=mongo_server)

asset_repository = AssetRepository(db_name="TradingConfig",uri=mongo_server)

relation_repository = RelationRepository(db_name="TradingConfig",uri=mongo_server)

news_repository = NewsRepository("News",mongo_server)

backtest_repository = BacktestRepository(db_name="Backtest",uri=mongo_server)

# Manager


asset_manager = AssetManager(asset_respository=asset_repository)

relation_manager = RelationManager(relation_repository=relation_repository,asset_manager=asset_manager,asset_repository=asset_repository)

trade_manager = TradeManager(trade_repository=trade_repository,broker_facade=broker_facade,risk_manager=risk_manager,relation_manager=relation_manager)

strategy_manager = StrategyRegistry()

config_manager = ConfigManager(trade_manager=trade_manager,asset_manager=asset_manager,relation_manager=relation_manager,strategy_manager=strategy_manager)

strategy_manager = StrategyRegistry()

# Handler

backtest_service = BacktestService(backtest_repository=backtest_repository)

new_file_handler = FileHandler(asset_manager=asset_manager,strategy_manager=strategy_manager,backtest_service=backtest_service)

# services

news_service = NewsService(news_repository=news_repository)


trading_service = TradingService(asset_manager=asset_manager,trade_manager=trade_manager,strategy_manager=strategy_manager,news_service=news_service)

# controller

signal_controller = SignalController(trading_service=trading_service, news_service=news_service,asset_manager=asset_manager, trade_manager=trade_manager,relation_manager=relation_manager,backtest_service=backtest_service)

# Logic

config_manager.initialize_managers()

schedule_manager = ScheduleService()

schedule_manager.every_day_add_schedule("News","12:00",news_service.run_news_scheduler)

news_service.fetch_news()

def MonitorFolder(handler, folderPath):
    observer = Observer()
    observer.schedule(handler, path=folderPath, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keeps the script running

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

thread = Thread(target=partial(MonitorFolder, new_file_handler, "incomingFiles"))
thread.start()

# thread2 = Thread(target=partial(backtest_service.fetch_test_assets))
# thread2.start()
