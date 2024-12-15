import datetime
import time
from functools import partial
from threading import Thread

import pytz
from watchdog.observers import Observer

from Controller.SignalController import SignalController
from Core.Pattern.Factory.StrategyFactory import StrategyFactory
from Services.DB.SubModules.mongoDBConfig import mongoDBConfig
from Services.DB.SubModules.mongoDBData import mongoDBData
from Services.DB.SubModules.mongoDBTrades import mongoDBTrades
from Services.DB.DBService import DBService
from Services.Helper.ConfigManager import ConfigManager
from Services.Helper.FileHandler import NewFileHandler
from Services.Helper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager
from Services.Manager.AssetManager import AssetManager
from Core.Main.Strategy.FrameWorkStorage.LevelHandler import LevelHandler
from Core.Main.Strategy.FrameWorkStorage.PDArrayHandler import PDArrayHandler
from Core.Main.Strategy.FrameWorkStorage.StructureHandler import StructureHandler
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.RiskHandler import RiskManager
from Services.Manager.TradeManager import TradeManager
from Services.TradingService import TradingService

ny_tz = pytz.timezone('America/New_York')

# DB

secretsManager = SecretsManager()

mapper = Mapper()

mongoDBTrades = mongoDBTrades(secretsManager, mapper)
mongoDBData = mongoDBData(secretsManager, mapper)
mongoDBConfig = mongoDBConfig(secretsManager, mapper)

dbService = DBService(mapper, mongoDBData, mongoDBTrades)

# Factory

strategyFactory = StrategyFactory()

# Handler

pdArrayHandler = PDArrayHandler()

levelHandler = LevelHandler()

structureHandler = StructureHandler()

# Manager / Services
assetManager = AssetManager(dbService)

strategyManager = StrategyManager(pdArrayHandler,levelHandler,structureHandler)

riskManager = RiskManager(2, 1)


tradeManager = TradeManager(dbService, strategyManager, riskManager)

tradingService = TradingService(assetManager, tradeManager, strategyManager)

configManager = ConfigManager(mongoDBConfig,assetManager,strategyManager,strategyFactory)

# FileHandler
newFileHandler = NewFileHandler(assetManager,strategyManager)

# Controller

signalController = SignalController(tradingService)

# Logic

configManager.runStartingSetup()


def monitorFolder(handler, folderPath):
    observer = Observer()
    observer.schedule(handler, path=folderPath, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keeps the script running

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def job(tradingService):
    # Hole die aktuelle Zeit in der New York-Zeitzone
    while True:
        time.sleep(20)
        now = datetime.datetime.now(ny_tz)
        # print(now.strftime("%H:%M"))
        # Wenn es 00:00 New York-Zeit ist
        if now.strftime("%H:%M") == "00:00":
            tradingService.executeDailyTasks()

#tradingService.executeDailyTasks()

# Use partial to pass tradingService as an argument
thread = Thread(target=partial(job, tradingService))
thread.start()


thread = Thread(target=partial(monitorFolder, newFileHandler, "/Users/lauris/PycharmProjects/AutomatedTrading/ObservedFolder"))
thread.start()
