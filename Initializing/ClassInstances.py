import datetime
import time
from functools import partial
from threading import Thread

import pytz

from Controller.SignalController import SignalControler
from Models.Asset.Asset import Asset
from Models.Broker.Bybit import Bybit
from Models.Strategy.Entry.FVGEntry import FVGEntry
from Models.Strategy.Exit.FVGExit import FVGExit
from Models.Strategy.Main.FVGSession import FVGSession
from Services.DB.mongoDBData import mongoDBData
from Services.DB.mongoDBTrades import mongoDBTrades
from Services.DBService import DBService
from Services.Helper.Mapper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager
from Services.Manager.AssetManager import AssetManager
from Services.Manager.RiskManager import RiskManager
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.TradeManager import TradeManager
from Services.TradingService import TradingService

ny_tz = pytz.timezone('America/New_York')

# Broker
bybit = Bybit("Bybit")

brokerNameList = [bybit.name]  # Crypto

# Strategy

fvgEntry = FVGEntry("FVGEntry")
fvgExit = FVGExit("FVGExit")

fvgSession = FVGSession("FVGSession", fvgExit, fvgEntry)

# Asset

timeFrameList = [1, 5, 15]  # 1, 5, 15 Scalping

smtPairNameList = ["USDT"]

btc = Asset("BTCUSDT.P", fvgSession.name, smtPairNameList, brokerNameList, timeFrameList)

#  #  Services

# DB

secretsManager = SecretsManager()

mapper = Mapper()

mongoDBTrades = mongoDBTrades(secretsManager, mapper)
mongoDBData = mongoDBData(secretsManager, mapper)

dbService = DBService(mapper, mongoDBData, mongoDBTrades)

# Manager / Services
strategyManager = StrategyManager()

assetManager = AssetManager(dbService)

riskManager = RiskManager(2, 1)

tradeManager = TradeManager(dbService)

tradingService = TradingService(assetManager, tradeManager, strategyManager)

# Controller

signalController = SignalControler(tradingService)

# Logic

assetManager.registerAsset(btc)

strategyManager.registerStrategy(fvgSession)


# tradingService.findOpenTrades()

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
