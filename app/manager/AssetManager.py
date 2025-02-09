import threading

from app.db.mongodb.MongoDBData import MongoDBData
from app.models.asset.Asset import Asset
from app.models.asset.Relation import Relation
from app.models.asset.Candle import Candle
from app.models.asset.SMTPair import SMTPair
from app.monitoring.logging.logging_startup import logger


class AssetManager:
    """
    Manages and centralizes operations related to financial assets.

    This singleton class serves as the central repository for managing assets, including
    registration, CRUD operations on candle data, and retrieval of asset-specific information
    or relationships. It ensures safe concurrent access and provides utility methods for interacting
    with the stored resources.

    :ivar assets: A dictionary holding the registered assets, with asset names as keys and Asset
        objects as values.
    :type assets: dict[str, Asset]
    :ivar _mongo_db_data: MongoDB data handler for interacting with the database.
    :type _mongo_db_data: MongoDBData
        systems and internal representations.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AssetManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.assets: dict[str,Asset] = {}
            self._mongo_db_data = MongoDBData()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Register And Return Assets
    def register_asset(self, asset: Asset) -> bool:
        logger.info(f"Register Asset to Asset Manager:{asset.name}")

        if not asset in self.assets:
            self.assets[asset.name] = asset
            logger.info("Registered asset {}".format(asset.name))
            return True
        logger.warning("Asset {} already registered".format(asset.name))
        return False

    def return_all_assets(self)->list[Asset]:
        return [x for x in self.assets.values()]

    # endregion

    # region CRUD

    def _add_candle_to_db(self, candle: Candle):
        logger.debug(f"Adding candle to db:{candle.asset}")
        try:
            self._mongo_db_data.add_candle_to_db(candle.asset, candle)
        except Exception as e:
            logger.critical("Failed to add candle to db with exception {}".format(e))

    def received_candles(self, asset: str):
        if asset in self.assets:
            logger.debug(f"Adding candle to db:{asset}")
            try:
                candles_db = self._mongo_db_data.receive_asset_data(asset)
                candles = []
                for candle_db in candles_db:
                    candles.append(Candle.model_validate(candle_db))

                for candle in candles:
                    self.assets[candle.asset].add_candle(candle)

            except Exception as e:
                logger.critical("Failed to add candle to db with exception {}".format(e))

    # endregion

    # region Add Functions
    def add_candle(self, json: dict) -> Candle:
        try:
            candle: Candle = Candle.model_validate(json)
            logger.debug(f"Add Candle to:{candle.asset}")

            if candle.asset in self.assets:
                self.assets[candle.asset].add_candle(candle)
                self._add_candle_to_db(candle)
                return candle
        except Exception as e:
            logger.exception("Failed to add candle to db with exception {}".format(e))

    def add_relation(self, relation: Relation):
        try:
            if relation.asset in self.assets:
                self.assets[relation.asset].add_relation(relation)
        except Exception as e:
            logger.exception("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def add_smt_pair(self, asset: str, smt_pair: SMTPair):
        try:
            if asset in self.assets:
                self.assets[asset].add_smt_pair(smt_pair)
        except Exception as e:
            logger.exception("Failed to add smt pair to asset {asset},Error:{e}".format(asset=asset, e=e))

    # endregion

    # region Return Functions

    def return_asset_class(self, asset: str) -> str:
        try:
            if asset in self.assets:
                return self.assets[asset].asset_class
        except Exception as e:
            logger.exception("Failed to return asset class for asset {asset},Error:{e}".format(asset=asset, e=e))

    def return_relations(self, asset: str,broker:str) -> list[Relation]:
        try:
            if asset in self.assets:
                return self.assets[asset].return_relations(broker)
        except Exception as e:
            logger.exception("Failed to return relations for asset:{asset},Error {e}".format(asset=asset, e=e))

    def return_candles(self, asset: str, broker: str, timeFrame: int) -> list[Candle]:
        try:
            if asset in self.assets:
                return self.assets[asset].return_candles(timeFrame, broker)
        except Exception as e:
            logger.exception("Failed to return candles for asset {asset},Error {e}".format(asset=asset, e=e))

    def return_all_relations(self, asset: str):
        try:
            if asset in self.assets:
                return self.assets[asset].relations
        except Exception as e:
            logger.exception("Failed to return relations for asset{asset},Error {e}".format(asset=asset, e=e))
    # endregion
