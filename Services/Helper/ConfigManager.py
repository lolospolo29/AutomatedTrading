
from Core.Main.Asset.Asset import Asset
from Core.Main.Asset.SubModels.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Core.Main.Asset.SubModels.SMTPair import SMTPair
from Core.API.Brokers.Broker import Broker
from Core.Main.Strategy.Strategy import Strategy
from Core.Pattern.Factory.StrategyFactory import StrategyFactory
from Monitoring.TimeWrapper import logTime
from Services.DB.SubModules.mongoDBConfig import mongoDBConfig
from Services.Manager.AssetManager import AssetManager
from Services.Manager.StrategyManager import StrategyManager


class ConfigManager:
    def __init__(self, configDB: mongoDBConfig, assetManager: AssetManager,
                 strategyManager: StrategyManager, strategyFactory: StrategyFactory):

        self._MongoDBConfig: mongoDBConfig = configDB
        self._AssetManager: AssetManager = assetManager
        self._StrategyManager: StrategyManager = strategyManager
        self._StrategyFactory: StrategyFactory = strategyFactory
        self.assets: list[Asset] = []
        self.brokers: list[Broker] = []
        self.strategies: list[Strategy] = []
        self.relations: list[AssetBrokerStrategyRelation] = []
        self.smtPairs: list[SMTPair] = []
    @logTime
    def runStartingSetup(self):

        assets: list = self._MongoDBConfig.loadData("Asset",None)
        brokers: list = self._MongoDBConfig.loadData("Broker",None)
        strategies: list = self._MongoDBConfig.loadData("Strategy",None)
        assetBrokerStrategyRelations: list = self._MongoDBConfig.loadData("AssetBrokerStrategyRelation"
                                                                          ,None)
        smtPairs: list = self._MongoDBConfig.loadData("SMTPairs",None)

        self.addDataToList("Asset", assets)
        self.addDataToList("Broker", brokers)
        self.addDataToList("Strategy", strategies)
        self.addDataToList("AssetBrokerStrategyRelation",
                           assetBrokerStrategyRelations)
        self.addDataToList("SMTPairs", smtPairs)

        self.runOverList()

    def addDataToList(self, typ: str, dbList: list) -> None:
        for doc in dbList:

            self.isTypAssetAddAsset(typ, doc)
            self.isTypStrategyAddStrategy(typ,doc)
            self.isTypRelationAddRelation(typ,doc)
            self.isTypSMTPairAddPair(typ,doc)

    def isTypAssetAddAsset(self, typ: str, doc: dict) -> None:

        if typ == "Asset":

            asset: Asset = Asset((doc.get(typ)).get("name"))
            self.assets.append(asset)

    def isTypStrategyAddStrategy(self,typ: str, doc: dict) -> None:
        if typ == "Strategy":

            strategyDict = doc.get(typ)
            name = strategyDict.get("name")
            entry = strategyDict.get("entry")
            exit = strategyDict.get("exit")
            strategy: Strategy = self._StrategyFactory.returnClass(name,entry,exit)
            self.strategies.append(strategy)

    def isTypRelationAddRelation(self,typ: str,doc: dict) -> None:
        if typ == "AssetBrokerStrategyRelation":

            asset: str = self._MongoDBConfig.findById("Asset","assetId",(doc.get(typ)).get("assetId"),
                                                      "name")

            broker: str = self._MongoDBConfig.findById("Broker","brokerId",(doc.get(typ)).get("brokerId"),
                                                       "name")

            strategy: str = self._MongoDBConfig.findById("Strategy","strategyId",
                                                         (doc.get(typ)).get("strategyId"),"name")
            self.relations.append(AssetBrokerStrategyRelation(asset,broker,strategy))

    def isTypSMTPairAddPair(self, typ: str, doc: dict):
        if typ == "SMTPairs":
            strategy: str = self._MongoDBConfig.findById("Strategy", "strategyId",
                                                         (doc.get(typ)).get("strategyId"), "name")
            smtPairs: list = doc.get(typ).get("smtPairIds")

            smtPairList: list = []

            for pair in smtPairs:
                smtPairList.append(self._MongoDBConfig.findById("Asset", "assetId", pair,
                                             "name"))

            self.smtPairs.append(SMTPair(strategy,smtPairList,doc.get(typ).get("correlation")))
    @logTime
    def runOverList(self):
        for strategy in self.strategies:
            self._StrategyManager.registerStrategy(strategy)
        for asset in self.assets:
            for relation in self.relations:
                if relation.asset == asset.name:
                    asset.addBroker(relation.broker)
                    asset.addStrategy(relation.strategy)
                    asset.addBrokerStrategyAssignment(relation.broker, relation.strategy)
                    expectedTimeFrames: list = self._StrategyManager.returnExpectedTimeFrame(relation.strategy)

                    for expectedTimeFrame in expectedTimeFrames:
                        asset.addCandleSeries(expectedTimeFrame.timeFrame, expectedTimeFrame.maxLen,relation.broker)
            for smtPair in self.smtPairs:
                for pair in smtPair.smtPair:
                    if pair == asset.name:
                        asset.addSMTPair(smtPair)
            self._AssetManager.registerAsset(asset)
