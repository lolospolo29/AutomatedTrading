import threading

from app.db.mongodb.RelationRepository import RelationRepository
from app.helper.factories.StrategyFactory import StrategyFactory
from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.models.asset.Relation import Relation
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
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RelationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._relation_repository = RelationRepository()
            self._asset_manager = AssetManager()
            self._strategy_manager = StrategyManager()
            self._strategy_factory = StrategyFactory()
            self._initialized = True  # Markiere als initialisiert

    def create_relation(self,relation:Relation):
        try:
            strategy = self._strategy_factory.return_strategy(typ=relation.strategy)

            if strategy is None:
                return

            self._strategy_manager.register_strategy(relation=relation, strategy=strategy)
            logger.debug(f"Adding relation to asset:{relation.asset}")
            self._asset_manager.add_relation(relation)
            logger.debug(f"Adding relation to db:{relation}")
            self._relation_repository.add_relation(relation)

            self.add_timeframes_to_asset(relation=relation)

        except Exception as e:
            logger.critical("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def add_timeframes_to_asset(self,relation:Relation):

        exp_timeframes:list[ExpectedTimeFrame] = self._strategy_manager.return_expected_time_frame(relation=relation)

        for exp_timeframe in exp_timeframes:
            exp_timeframe:ExpectedTimeFrame = exp_timeframe

            self._asset_manager.add_candles_series(asset=relation.asset,timeframe=exp_timeframe.timeframe
                                                   ,maxlen=exp_timeframe.max_Len,broker=relation.broker)