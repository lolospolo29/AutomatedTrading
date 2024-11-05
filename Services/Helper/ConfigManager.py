from Models.Main.Asset.Asset import Asset
from Models.Main.Brokers.Broker import Broker
from Models.Main.Strategies.Strategy import Strategy
from Models.Pattern.Factory.BrokerFactory import BrokerFactory
from Models.Pattern.Factory.StrategyFactory import StrategyFactory
from Services.DB.mongoDBConfig import mongoDBConfig
from Services.Manager.AssetManager import AssetManager
from Services.Manager.BrokerManager import BrokerManager
from Services.Manager.StrategyManager import StrategyManager


class ConfigManager:
    def __init__(self, configDB: mongoDBConfig, assetManager: AssetManager, brokerManager: BrokerManager,
                 strategyManager: StrategyManager, brokerFactory: BrokerFactory, strategyFactory: StrategyFactory):
        self._MongoDBConfig: mongoDBConfig = configDB
        self._AssetManager: AssetManager = assetManager
        self._BrokerManager: BrokerManager = brokerManager
        self._StrategyManager: StrategyManager = strategyManager
        self._BrokerFactory: BrokerFactory = brokerFactory
        self._StrategyFactory: StrategyFactory = strategyFactory

    def runStartingSetup(self):
        assets: list = self._MongoDBConfig.loadData("Asset")
        brokers: list = self._MongoDBConfig.loadData("Broker")
        strategies: list = self._MongoDBConfig.loadData("Strategy")
        assetBrokerStrategyRelations: list = self._MongoDBConfig.loadData("AssetBrokerStrategyRelation")
        smtPairs: list = self._MongoDBConfig.loadData("SMTPairs")

        assetDict = self.listToDict("Asset", assets)
        brokerDict = self.listToDict("Broker", brokers)
        strategiesDict = self.listToDict("Strategy", strategies)
        assetBrokerStrategyRelationDict = self.listToDict("AssetBrokerStrategyRelation",
                                                          assetBrokerStrategyRelations)
        smtPairDict = self.listToDict("SMTPairs", smtPairs)

    def listToDict(self,typ: str, dbList: list) -> dict:
        typDict = {}
        for doc in dbList:
            self.isTypAssetAddAsset(typ, doc)
            self.isTypBrokerAddBroker(typ, doc)
            self.isTypStrategyAddStrategy(typ,doc)
            typDict[(doc.get(typ)).get("name")] = (doc.get(typ))

        return typDict

    def isTypAssetAddAsset(self, typ: str, doc: dict) -> None:
        if typ == "Asset":
            asset: Asset = Asset((doc.get(typ)).get("name"))
            self._AssetManager.registerAsset(asset)

    def isTypBrokerAddBroker(self, typ: str, doc: dict) -> None:
        if typ == "Brokers":
            broker: Broker = self._BrokerFactory.returnClass((doc.get(typ)).get("name"))
            self._BrokerManager.registerBroker(broker)

    def isTypStrategyAddStrategy(self,typ: str, doc: dict) -> None:
        if typ == "Strategy":
            strategyDict = doc.get(typ)
            name = strategyDict.get("name")
            entry = strategyDict.get("entry")
            exit = strategyDict.get("exit")
            strategy: Strategy = self._StrategyFactory.returnClass(name,entry,exit)
            self._StrategyManager.registerStrategy(strategy)
