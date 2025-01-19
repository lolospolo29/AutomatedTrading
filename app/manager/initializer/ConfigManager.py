import os
import threading

from app.db.mongodb.mongoDBConfig import mongoDBConfig
from app.db.mongodb.mongoDBTrades import mongoDBTrades
from app.helper.factories.StrategyFactory import StrategyFactory
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.SMTPair import SMTPair
from app.models.strategy.Strategy import Strategy
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.log_time import log_time
from app.monitoring.logging.logging_startup import logger


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

        self._mongo_db_config: mongoDBConfig = mongoDBConfig()
        self._mongo_db_trades: mongoDBTrades = mongoDBTrades()
        self._trade_manager: TradeManager = TradeManager()
        self._trade_semaphore_registry: TradeSemaphoreRegistry = TradeSemaphoreRegistry()
        self._asset_manager: AssetManager = AssetManager()
        self._strategy_manager: StrategyManager = StrategyManager()
        self._strategy_factory: StrategyFactory = StrategyFactory()
        self._assets: list[Asset] = []
        self._brokers: list = []
        self._strategies: list[Strategy] = []
        self._relations: list[AssetBrokerStrategyRelation] = []
        self._smtPairs: list[SMTPair] = []
        self._trades: list[Trade] = []
        self._Orders: list[Order] = []
        self._asset_classes: dict[int, str] = {}

    # endregion

    # region Starting Setup
    @log_time
    def run_starting_setup(self):

        logger.info("Initializing ConfigManager")
        try:

            assets: list = self._mongo_db_config.load_data("Asset", None)
            brokers: list = self._mongo_db_config.load_data("Broker", None)
            strategies: list = self._mongo_db_config.load_data("Strategy", None)
            relations: list = self._mongo_db_config.load_data("AssetBrokerStrategyRelation"
                                                              , None)
            smtPairs: list = self._mongo_db_config.load_data("SMTPairs", None)
            asset_classes:list = self._mongo_db_config.load_data("AssetClasses", None)

            trades: list = self._mongo_db_trades.find_trade_or_trades_by_id()

            self._trades.extend(trades)

            # todo fix

            self._add_data_to_list("AssetClass", asset_classes)
            self._add_data_to_list("Asset", assets)
            self._add_data_to_list("Broker", brokers)
            self._add_data_to_list("Strategy", strategies)
            self._add_data_to_list("AssetBrokerStrategyRelation",
                                   relations)
            self._add_data_to_list("SMTPairs", smtPairs)

            self._initialize_managers()
        except Exception as e:
            logger.exception("Fatal Error in ConfigManager")
            os._exit(1)
        finally:
            logger.info("Finished ConfigManager")

    def _initialize_managers(self):
        for strategy in self._strategies:
                for relation in self._relations:
                    try:
                        if relation.strategy == strategy:
                            self._strategy_manager.register_strategy(relation, strategy)
                    except Exception as e:
                        logger.warning("Failed to register strategy {}".format(strategy.name))
                    finally:
                        continue
        for asset in self._assets:
            try:
                for relation in self._relations:
                    try:
                        if relation.asset == asset.name:
                            asset.add_broker(relation.broker)
                            asset.add_strategy(relation.strategy)
                            asset.add_relation(relation)
                            self._trade_semaphore_registry.register_relation(relation)
                            expectedTimeFrames: list = self._strategy_manager.return_expected_time_frame(relation.strategy)

                            for expectedTimeFrame in expectedTimeFrames:
                                asset.add_candle_series(expectedTimeFrame.timeframe, expectedTimeFrame.max_Len,
                                                        relation.broker)
                    except Exception as e:
                        logger.warning("Failed to register asset {}".format(asset.name))
                for smtPair in self._smtPairs:
                        for pair in smtPair.smt_pairs:
                            if pair == asset.name:
                                asset.add_smt_pair(smtPair)
                self._asset_manager.register_asset(asset)
            except Exception as e:
                logger.warning("Failed to register asset {}".format(asset.name))
            finally:
                continue
        for trade in self._trades:
            try:
                self._trade_manager.register_trade(trade)
            except Exception as e:
                logger.exception("Failed to register trade {}".format(trade.id))

    # endregion

    # region Checkings
    def _add_data_to_list(self, typ: str, dbList: list) -> None:
        for doc in dbList:
            try:
                self._is_typ_asset_add_asset(typ, doc)
                self._is_typ_strategy_add_strategy(typ, doc)
                self._is_typ_relation_add_relation(typ, doc)
                self._is_typ_smt_pair_add_pair(typ, doc)
                self._is_typ_asset_class(typ, doc)
            except Exception as e:
                logger.warning("Failed within doc {}".format(doc.id))
            finally:
                continue
    def _is_typ_asset_add_asset(self, typ: str, doc: dict) -> None:
        if typ == "Asset":
            asset: Asset = Asset((doc.get(typ)).get("name"), self._asset_classes[doc.get(typ).get("assetClass")])
            self._assets.append(asset)
            logger.debug("Asset {} from database".format(asset.name))

    def _is_typ_strategy_add_strategy(self, typ: str, doc: dict) -> None:
        if typ == "Strategy":
            strategyDict = doc.get(typ)
            name = strategyDict.get("name")
            strategy: Strategy = self._strategy_factory.return_class(name)
            self._strategies.append(strategy)
            logger.debug("Strategy {} from database".format(strategy.name))

    def _is_typ_relation_add_relation(self, typ: str, doc: dict) -> None:
        if typ == "AssetBrokerStrategyRelation":

            asset: str = self._mongo_db_config.find_by_id("Asset", "assetId", (doc.get(typ)).get("assetId"),
                                                      "name")

            broker: str = self._mongo_db_config.find_by_id("Broker", "brokerId", (doc.get(typ)).get("brokerId"),
                                                       "name")

            strategy: str = self._mongo_db_config.find_by_id("Strategy", "strategyId",
                                                             (doc.get(typ)).get("strategyId"),"name")
            maxTrades = doc.get(typ)["maxTrades"]
            self._relations.append(AssetBrokerStrategyRelation(asset, broker, strategy,maxTrades))
            logger.debug("Relation from database {}".format(asset))

    def _is_typ_smt_pair_add_pair(self, typ: str, doc: dict)->None:
        if typ == "SMTPairs":
            strategy: str = self._mongo_db_config.find_by_id("Strategy", "strategyId",
                                                             (doc.get(typ)).get("strategyId"), "name")
            smtPairs: list = doc.get(typ).get("smtPairIds")

            smtPairList: list[str] = []

            for pair in smtPairs:
                smtPairList.append(self._mongo_db_config.find_by_id("Asset", "assetId", pair,
                                             "name"))

            self._smtPairs.append(SMTPair(strategy, smtPairList, doc.get(typ).get("correlation")))
            logger.debug("SMTPair {} from database".format(str(smtPairList)))

    def _is_typ_asset_class(self, typ: str, doc: dict)->None:
        if typ == "AssetClass":
            self._asset_classes[doc.get(typ).get("assetClassId")] = doc.get(typ).get("name")
            logger.debug("Asset class {} from database".format(doc.get(typ).get("assetClass")))

    # endregion

