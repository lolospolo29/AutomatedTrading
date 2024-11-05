import datetime
import time
from functools import partial
from threading import Thread

import pytz

from Controller.SignalController import SignalControler
from Services.DB.mongoDBData import mongoDBData
from Services.DB.mongoDBTrades import mongoDBTrades
from Services.DBService import DBService
from Services.Helper.Mapper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager
from Services.Manager.AssetManager import AssetManager
from Services.Manager.BrokerManager import BrokerManager
from Services.Manager.RiskManager import RiskManager
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.TradeManager import TradeManager
from Services.TradingService import TradingService

ny_tz = pytz.timezone('America/New_York')

#  #  Services

# DB

secretsManager = SecretsManager()

mapper = Mapper()

mongoDBTrades = mongoDBTrades(secretsManager, mapper)
mongoDBData = mongoDBData(secretsManager, mapper)

dbService = DBService(mapper, mongoDBData, mongoDBTrades)

# Manager / Services
assetManager = AssetManager(dbService)

strategyManager = StrategyManager(assetManager)

riskManager = RiskManager(2, 1)

brokerManager = BrokerManager()

tradeManager = TradeManager(dbService, brokerManager, strategyManager, riskManager)

tradingService = TradingService(assetManager, tradeManager, strategyManager)

# Controller

signalController = SignalControler(tradingService)

# Logic

def job(trading_service):
    # Hole die aktuelle Zeit in der New York-Zeitzone
    while True:
        time.sleep(20)
        now = datetime.datetime.now(ny_tz)
        print(now.strftime("%H:%M"))
        # Wenn es 00:00 New York-Zeit ist
        if now.strftime("%H:%M") == "00:00":
            trading_service.executeDailyTasks()


# Use partial to pass tradingService as an argument
thread = Thread(target=partial(job, tradingService))
thread.start()
