import time
from functools import partial
from threading import Thread

from watchdog.observers import Observer

from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.controller.SignalController import SignalController
from app.db.mongodb.AssetRepository import AssetRepository
from app.db.mongodb.BacktestRepository import BacktestRepository
from app.db.mongodb.NewsRepository import NewsRepository
from app.db.mongodb.RelationRepository import RelationRepository
from app.db.mongodb.TradeRepository import TradeRepository
from app.helper.registry.BrokerRegistry import BrokerRegistry
from app.helper.manager.AssetManager import AssetManager
from app.helper.manager.RelationManager import RelationManager
from app.helper.manager.RiskManager import RiskManager
from app.helper.registry.StrategyRegistry import StrategyManager
from app.helper.manager.TradeManager import TradeManager
from app.helper.manager.initializer.SecretsManager import SecretsManager
from app.services.BacktestService import BacktestService
from app.services.NewsService import NewsService
from app.services.ScheduleService import ScheduleService
from app.services.TradingService import TradingService
from tools.FileHandler import FileHandler
from app.helper.manager.initializer.ConfigManager import ConfigManager

# Broker

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

strategy_manager = StrategyManager()

config_manager = ConfigManager(trade_manager=trade_manager,asset_manager=asset_manager,relation_manager=relation_manager,strategy_manager=strategy_manager)

strategy_manager = StrategyManager()

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

thread = Thread(target=partial(MonitorFolder, new_file_handler, "/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles"))
thread.start()
