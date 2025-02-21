import threading

from app.db.mongodb.AssetRepository import AssetRepository
from app.db.mongodb.RelationRepository import RelationRepository
from app.db.mongodb.TradeRepository import TradeRepository
from app.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.helper.factories.StrategyFactory import StrategyFactory
from app.manager.AssetManager import AssetManager
from app.manager.RelationManager import RelationManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.asset.Relation import Relation
from app.models.asset.SMTPair import SMTPair
from app.models.strategy.Strategy import Strategy
from app.models.trade.Trade import Trade
from app.monitoring.log_time import log_time
from app.monitoring.logging.logging_startup import logger


class ConfigManager:
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,trade_manager:TradeManager,asset_manager:AssetManager,relation_manager:RelationManager):

        self._trade_manager: TradeManager = trade_manager
        self._asset_manager: AssetManager = asset_manager
        self._relation_manager: RelationManager = relation_manager
        self._strategy_manager: StrategyManager = StrategyManager()
        self._strategy_factory: StrategyFactory = StrategyFactory()

    # endregion

    # region Starting Setup
    @log_time
    def run_starting_setup(self):
        logger.info("Initializing ConfigManager")

        assets_dtos = self._asset_repository.find_assets()

        for asset_dto in assets_dtos:
            try:
                asset_dto:AssetDTO = asset_dto

                ### Register Asset

                asset_class_dto :AssetClassDTO= self._asset_repository.find_asset_class_by_id(asset_dto.assetClass)

                asset:Asset =  Asset(name=asset_dto.name,asset_class=asset_class_dto.name,smt_pairs=[],relations=[],candles_series=[],asset_id=asset_dto.assetId)

                self._asset_manager.register_asset(asset)

                ####

                relations_db: list = self._relation_repository.find_relations_by_asset_id(asset_dto.assetId)

                for relation_db in relations_db:

                    ## Add Relation

                    try:

                        relation_dto:RelationDTO = relation_db

                        broker_dto:BrokerDTO = self._relation_repository.find_broker_by_id(relation_db.brokerId)

                        strategy_dto:StrategyDTO = self._relation_repository.find_strategy_by_id(relation_db.strategyId)

                        relation = Relation(asset=asset_dto.name,strategy=strategy_dto.name,broker=broker_dto.name,max_trades=relation_dto.maxTrades,id=relation_dto.relationId)

                        self._asset_manager.add_relation(relation)

                        ###

                        smt_pair_dtos:list[SMTPairDTO] = self._asset_repository.find_smt_pair_by_id(assetAId=relation_dto.assetId
                                                                                 ,strategyId=relation_dto.strategyId,assetBId=None)

                        smt_pair_dtos.extend(self._asset_repository.find_smt_pair_by_id(assetAId=None
                                                                                       ,assetBId=relation_dto.assetId
                                                                                       ,strategyId=None))

                        self.register_strategy(relation=relation, asset_dto=asset_dto
                                               , smt_pair_dtos=smt_pair_dtos)

                        self._relation_manager.add_timeframes_to_asset(relation=relation)

                        ###

                        trades_db: list[TradeDTO] = self._trade_repository.find_trades()

                        for trade_db in trades_db:
                            trade_db:TradeDTO = trade_db
                            orders = []
                            if trade_db.relationId == relation_dto.relationId:
                                try:
                                    orders.extend(self._trade_repository.find_orders_by_trade_id(trade_db.tradeId))

                                    trade = Trade(orders=orders, tradeId=trade_db.tradeId, relation=relation, category=trade_db.category
                                                  , side=trade_db.side, tpslMode=trade_db.tpslMode,
                                                  unrealisedPnl=trade_db.unrealisedPnl
                                                  , leverage=trade_db.leverage, size=trade_db.size, tradeMode=trade_db.tradeMode
                                                  , updatedTime=trade_db.updatedTime, createdTime=trade_db.createdTime)

                                    self._trade_manager.register_trade(trade)
                                except Exception as e:
                                    logger.info("Error in Config Manager while registering trades: {e}".format(e=e))
                                finally:
                                    continue
                    except Exception as e:
                        logger.info("Error in Config Manager while registering relations: {e}".format(e=e))
            except Exception as e:
                logger.info("Error in Config Manager while registering assets: {e}".format(e=e))
            finally:
                continue
        logger.info("ConfigManager initialized")

    def register_strategy(self, relation:Relation, asset_dto:AssetDTO
                          , smt_pair_dtos:list[SMTPairDTO]):

        if len(smt_pair_dtos) > 0:
            for smt_pair_dto in smt_pair_dtos:
                smt_pair_dto: SMTPairDTO = smt_pair_dto

                smt_strategy, smt_pair = self.create_smt(asset_dto=asset_dto, relation=relation, smt_pair_dto=smt_pair_dto)
                if smt_strategy is None:
                    logger.error("SMT Strategy has None Type. Skipping.")
                    return
                self._strategy_manager.register_smt_strategy(relation_smt=relation, strategy_smt=smt_strategy,
                                                             asset2=smt_pair.asset_b)

                self._asset_manager.add_smt_pair(asset=relation.asset,smt_pair=smt_pair)


        elif len(smt_pair_dtos) == 0:
            strategy = self._strategy_factory.return_strategy(typ=relation.strategy)

            self._strategy_manager.register_strategy(relation=relation, strategy=strategy)

    def create_smt(self, asset_dto:AssetDTO, relation:Relation, smt_pair_dto:SMTPairDTO)->tuple[Strategy,SMTPair]:
        asset_b: AssetDTO = AssetDTO(name="", assetId=-1)

        if smt_pair_dto.assetAId == asset_dto.assetId:
            asset_b: AssetDTO = self._asset_repository.find_asset_by_id(smt_pair_dto.assetBId)

        if smt_pair_dto.assetBId == asset_dto.assetId:
            asset_b: AssetDTO = self._asset_repository.find_asset_by_id(smt_pair_dto.assetAId)

        smt_strategy: Strategy = self._strategy_factory.return_smt_strategy(typ=relation.strategy
                                                                             ,correlation=smt_pair_dto.correlation,
                                                                             asset1=relation.asset
                                                                             , asset2=asset_b.name)

        smt_pair: SMTPair = SMTPair(strategy=relation.strategy, asset_a=asset_dto.name, asset_b=asset_b.name,
                                    correlation=smt_pair_dto.correlation)

        return smt_strategy,smt_pair
    # endregion
