import threading

from app.api.Brokers.Broker import Broker
from app.db.modules.mongoDBConfig import mongoDBConfig
from app.helper.factories.StrategyFactory import StrategyFactory
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.models.asset.Asset import Asset
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.SMTPair import SMTPair
from app.models.strategy.Strategy import Strategy
from app.monitoring.TimeWrapper import logTime


class ConfigManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing
    def __init__(self):

        self._MongoDBConfig: mongoDBConfig = mongoDBConfig()
        self._AssetManager: AssetManager = AssetManager()
        self._StrategyManager: StrategyManager = StrategyManager()
        self._StrategyFactory: StrategyFactory = StrategyFactory()
        self._assets: list[Asset] = []
        self._brokers: list[Broker] = []
        self._strategies: list[Strategy] = []
        self._relations: list[AssetBrokerStrategyRelation] = []
        self._smtPairs: list[SMTPair] = []

    # endregion

    # region Starting Setup
    @logTime
    def runStartingSetup(self):

        assets: list = self._MongoDBConfig.loadData("asset",None)
        brokers: list = self._MongoDBConfig.loadData("Broker",None)
        strategies: list = self._MongoDBConfig.loadData("strategy",None)
        assetBrokerStrategyRelations: list = self._MongoDBConfig.loadData("AssetBrokerStrategyRelation"
                                                                          ,None)
        smtPairs: list = self._MongoDBConfig.loadData("SMTPairs",None)

        self._addDataToList("asset", assets)
        self._addDataToList("Broker", brokers)
        self._addDataToList("strategy", strategies)
        self._addDataToList("AssetBrokerStrategyRelation",
                            assetBrokerStrategyRelations)
        self._addDataToList("SMTPairs", smtPairs)

        self._InitializeManagers()

    @logTime
    def _InitializeManagers(self):
        for strategy in self._strategies:
            self._StrategyManager.registerStrategy(strategy)
        for asset in self._assets:
            for relation in self._relations:
                if relation.asset == asset.name:
                    asset.addBroker(relation.broker)
                    asset.addStrategy(relation.strategy)
                    asset.addBrokerStrategyAssignment(relation.broker, relation.strategy)
                    expectedTimeFrames: list = self._StrategyManager.returnExpectedTimeFrame(relation.strategy)

                    for expectedTimeFrame in expectedTimeFrames:
                        asset.addCandleSeries(expectedTimeFrame.timeFrame, expectedTimeFrame.maxLen,relation.broker)
            for smtPair in self._smtPairs:
                for pair in smtPair.smtPairs:
                    if pair == asset.name:
                        asset.addSMTPair(smtPair)
            self._AssetManager.registerAsset(asset)
    # endregion

    # region Checkings
    def _addDataToList(self, typ: str, dbList: list) -> None:
        for doc in dbList:

            self._isTypAssetAddAsset(typ, doc)
            self._isTypStrategyAddStrategy(typ, doc)
            self._isTypRelationAddRelation(typ, doc)
            self._isTypSMTPairAddPair(typ, doc)

    def _isTypAssetAddAsset(self, typ: str, doc: dict) -> None:

        if typ == "asset":

            asset: Asset = Asset((doc.get(typ)).get("name"))
            self._assets.append(asset)

    def _isTypStrategyAddStrategy(self, typ: str, doc: dict) -> None:
        if typ == "strategy":

            strategyDict = doc.get(typ)
            name = strategyDict.get("name")
            entry = strategyDict.get("entry")
            exit = strategyDict.get("exit")
            strategy: Strategy = self._StrategyFactory.returnClass(name,entry,exit)
            self._strategies.append(strategy)

    def _isTypRelationAddRelation(self, typ: str, doc: dict) -> None:
        if typ == "AssetBrokerStrategyRelation":

            asset: str = self._MongoDBConfig.findById("asset","assetId",(doc.get(typ)).get("assetId"),
                                                      "name")

            broker: str = self._MongoDBConfig.findById("Broker","brokerId",(doc.get(typ)).get("brokerId"),
                                                       "name")

            strategy: str = self._MongoDBConfig.findById("strategy","strategyId",
                                                         (doc.get(typ)).get("strategyId"),"name")
            self._relations.append(AssetBrokerStrategyRelation(asset, broker, strategy))

    def _isTypSMTPairAddPair(self, typ: str, doc: dict)->None:
        if typ == "SMTPairs":
            strategy: str = self._MongoDBConfig.findById("strategy", "strategyId",
                                                         (doc.get(typ)).get("strategyId"), "name")
            smtPairs: list = doc.get(typ).get("smtPairIds")

            smtPairList: list = []

            for pair in smtPairs:
                smtPairList.append(self._MongoDBConfig.findById("asset", "assetId", pair,
                                             "name"))

            self._smtPairs.append(SMTPair(strategy, smtPairList, doc.get(typ).get("correlation")))
    # endregion

