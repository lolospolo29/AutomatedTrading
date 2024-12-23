import datetime
import time
from functools import partial
from threading import Thread

import pytz
from watchdog.observers import Observer

ny_tz = pytz.timezone('America/New_York')

tradeManager = TradeManager(dbService, strategyManager, riskManager)

tradingService = TradingService(assetManager, tradeManager, strategyManager)

configManager = ConfigManager(mongoDBConfig,assetManager,strategyManager,strategyFactory)

# FileHandler
newFileHandler = FileHandler(assetManager, strategyManager)

# controller

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

thread = Thread(target=partial(monitorFolder, newFileHandler, "/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles"))
thread.start()
