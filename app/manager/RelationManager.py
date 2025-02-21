import threading

from app.db.mongodb.AssetRepository import AssetRepository
from app.db.mongodb.RelationRepository import RelationRepository
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from app.helper.factories.StrategyFactory import StrategyFactory
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.models.asset.Relation import Relation
from app.models.asset.SMTPair import SMTPair
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.monitoring.logging.logging_startup import logger


class RelationManager:
    """
    Manages relationships between assets, strategies, and timeframes by coordinating
    with the repository, asset manager, and strategy manager. Provides functionality
    to create relations and append timeframes to assets.

    This singleton class ensures a centralized management of asset relationships
    and expected timeframes by using threading for safe instantiation. It aligns
    different components by interacting with asset data and strategies.

    """
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(RelationManager, cls).__new__(cls)
        return cls._instance


    def __init__(self,relation_repository:RelationRepository,asset_manager:AssetManager,asset_repository:AssetRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._relation_repository = relation_repository
            self._asset_repository = asset_repository
            self._asset_manager = asset_manager
            self._strategy_manager = StrategyManager()
            self._strategy_factory = StrategyFactory()
            self._initialized = True  # Markiere als initialisiert

    def return_relation_for_id(self,relation_id:int)->Relation:
        relation_dto:RelationDTO = self._relation_repository.find_relation_by_id(relation_id)

        asset_dto = self._relation_repository.find_asset_by_id(relation_dto.assetId)
        broker_dto = self._relation_repository.find_broker_by_id(relation_dto.brokerId)
        strategy_dto = self._relation_repository.find_strategy_by_id(relation_dto.strategyId)

        relation = Relation(asset=asset_dto.name, broker=broker_dto.name, strategy=strategy_dto.name
                            , max_trades=relation_dto.maxTrades, id=relation_dto.relationId)
        return relation


    def return_relations(self)->list[Relation]:
        relation_dtos:list[RelationDTO] = self._relation_repository.find_relations()

        relations:list[Relation] = []
        for relation_dto in relation_dtos:
            relations.append(self.return_relation_for_id(relation_dto.relationId))
        return relations

    def delete_relation(self,relation:Relation):
        self._asset_manager.remove_relation(relation=relation)
        self._strategy_manager.delete_strategy(relation=relation)
        self._relation_repository.delete_relation(relation=relation)

    def update_relation(self,relation:Relation):
        self._asset_manager.update_relation(relation=relation)
        self._strategy_manager.update_relation(relation=relation)
        self._relation_repository.update_relation(relation=relation)

    def create_relation(self,relation:Relation):
        try:
            self._relation_repository.add_relation(relation)
            self._asset_manager.add_relation(relation)

            strategy = self._strategy_factory.return_strategy(typ=relation.strategy)

            self._strategy_manager.register_strategy(relation=relation, strategy=strategy)
            logger.debug(f"Adding relation to asset:{relation.asset}")
            logger.debug(f"Adding relation to db:{relation}")

            self.add_timeframes_to_asset(relation=relation)

        except Exception as e:
            logger.critical("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def add_timeframes_to_asset(self,relation:Relation):

        exp_timeframes:list[ExpectedTimeFrame] = self._strategy_manager.return_expected_time_frame(relation=relation)

        for exp_timeframe in exp_timeframes:
            exp_timeframe:ExpectedTimeFrame = exp_timeframe

            self._asset_manager.add_candles_series(asset=relation.asset,timeframe=exp_timeframe.timeframe
                                                   ,maxlen=exp_timeframe.max_Len,broker=relation.broker)

    def create_smt(self,smt_pair:SMTPair):
        logger.info(f"Adding SMT,{smt_pair.asset_a},{smt_pair.asset_b},{smt_pair.correlation} to db and manager.")
        self._relation_repository.add_smt_pair(smt_pair=smt_pair)

        self._asset_manager.add_smt_pair(asset=smt_pair.asset_a,smt_pair=smt_pair)
        self._asset_manager.add_smt_pair(asset=smt_pair.asset_b,smt_pair=smt_pair)

        relations:list[Relation] = self.return_relations()

        for relation in relations:
            try:
                if ((relation.asset == smt_pair.asset_a or relation.asset == smt_pair.asset_b)
                        and smt_pair.strategy == relation.strategy):
                    strategy = self._strategy_factory.return_smt_strategy(typ=relation.strategy
                                                                          ,correlation=smt_pair.correlation
                                                                          ,asset2=smt_pair.asset_a
                                                                          ,asset1=smt_pair.asset_b)
                    if strategy is None:
                        return
                    asset_b = smt_pair.asset_b if relation.asset == smt_pair.asset_a else smt_pair.asset_a
                    self._strategy_manager.register_smt_strategy(relation_smt=relation, strategy_smt=strategy,asset2=asset_b)
                    self.add_timeframes_to_asset(relation=relation)
            except Exception as e:
                logger.critical("Failed to add SMT pair to db and manager. Error:{e}".format(e=e))
                continue

    # todo test smt
    def return_smt_pairs(self)->list[SMTPair]:
        smt_pair_dtos:list[SMTPairDTO] = self._relation_repository.find_smt_pairs()

        smt_pairs:list[SMTPair] = []

        for smt_pair_dto in smt_pair_dtos:
            try:
                smt_pair_dto:SMTPairDTO = smt_pair_dto

                asset_a_dto = self._asset_repository.find_asset_by_id(smt_pair_dto.assetAId)
                asset_b_dto = self._asset_repository.find_asset_by_id(smt_pair_dto.assetBId)
                strategy_dto = self._relation_repository.find_strategy_by_id(smt_pair_dto.strategyId)

                smt_pair = SMTPair(strategy=strategy_dto.name,asset_a=asset_a_dto.name,asset_b=asset_b_dto.name
                                   ,correlation=smt_pair_dto.correlation)

                smt_pairs.append(smt_pair)
            except Exception as e:
                logger.critical("Failed to add SMT pair to db and manager. Error:{e}".format(e=e))
                continue
        return smt_pairs

    def delete_smt_pair(self,smt_pair:SMTPair):
        logger.info(f"Removing SMT pair:{smt_pair.asset_a},{smt_pair.asset_b},{smt_pair.correlation} from db and manager.")

        relations:list[Relation] = self.return_relations()

        for relation in relations:
            if (relation.asset == smt_pair.asset_a or relation.asset == smt_pair.asset_a) and smt_pair.strategy == relation.strategy:
                self.delete_relation(relation=relation)

        self._relation_repository.delete_smt_pair(smt_pair=smt_pair)
