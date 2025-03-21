import threading
from logging import Logger

from files.db.mongodb.AssetRepository import AssetRepository
from files.db.mongodb.DataRepository import DataRepository
from files.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from files.db.mongodb.dtos.AssetDTO import AssetDTO
from files.models.asset.Asset import Asset
from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation
from files.models.asset.SMTPair import SMTPair

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
    :ivar _asset_respository: MongoDB data handler for interacting with the database.
    :type _asset_respository: MongoDBData
        systems and internal representations.
    """
    # region Initializing


    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(AssetManager, cls).__new__(cls)
        return cls._instance


    def __init__(self,asset_respository:AssetRepository,trading_data_repository:DataRepository,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.assets: dict[str,Asset] = {}
            self._asset_respository = asset_respository
            self._data_repository = trading_data_repository
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Registry Functions
    def add_asset(self, asset: Asset) -> bool:
        self._logger.info(f"Register Asset to Asset Manager:{asset.name}")

        if not asset.name in self.assets:
            self.assets[asset.name] = asset
            self._logger.info("Registered asset {}".format(asset.name))
            return True
        self._logger.warning("Asset {} already registered".format(asset.name))
        return False

    def remove_asset(self,asset:Asset):
        try:
            if asset.name in self.assets:
                del self.assets[asset.name]
                self._logger.info(f"Asset {asset.name} deleted")
        except Exception as e:
            self._logger.exception("Failed to delete asset {asset},Error:{e}".format(asset=asset, e=e))

    # endregion

    # region CRUD

    def return_asset_classes(self)->list[AssetClassDTO]:
        return self._asset_respository.find_asset_classes()

    def return_assets(self)->list[Asset]:
        dtos:list[AssetDTO] = self._asset_respository.find_assets()
        assets = []
        for dto in dtos:
            dto:AssetDTO = dto
            asset_class_dto: AssetClassDTO = self._asset_respository.find_asset_class_by_id(dto.assetClass)
            asset: Asset = Asset(name=dto.name, asset_class=asset_class_dto.name, smt_pairs=[], relations=[],
                                 candles_series=[], asset_id=dto.assetId)

            assets.append(asset)
        return assets

    def return_stored_assets(self)->list[Asset]:
        return [x for x in self.assets.values()]

    def create_asset(self,asset:Asset):
        try:
            if not asset.name in self.assets:
                self.add_asset(asset)
                self._logger.debug(f"Adding Asset to Asset Manager:{asset}")
                self._asset_respository.add_asset(asset)
                self._logger.debug(f"Adding Asset to db:{asset}")
        except Exception as e:
            self._logger.critical("Failed to add Asset to db with exception {}".format(e))

    def delete_asset(self,asset:Asset):
        try:
            if asset.name in self.assets:
                self.remove_asset(asset)
                self._logger.debug(f"Delete Asset:{asset}")
                self._asset_respository.delete_asset(asset)
                self._logger.debug(f"Delete Asset from db:{asset}")
        except Exception as e:
            self._logger.critical("Failed to delete Asset from db with exception {}".format(e))

    def update_asset(self,asset:Asset):
        try:
            dto:AssetDTO = self._asset_respository.find_asset_by_id(asset.asset_id)
            if dto.name in self.assets:
                self.assets[asset.name].update_asset(asset)
                self._logger.debug(f"Update Asset in Asset Manager:{asset}")
                self._asset_respository.update_asset(asset)
                self._logger.debug(f"Update Asset in db:{asset}")
        except Exception as e:
            self._logger.critical("Failed to update Asset with exception {}".format(e))

    # endregion

    # region Add Functions

    def _add_candle_to_db(self, candle: Candle):
        self._logger.debug(f"Adding candle to db:{candle.asset}")
        try:
            self._data_repository.add_candle(candle.asset, candle)
        except Exception as e:
            self._logger.critical("Failed to add candle to db with exception {}".format(e))

    def add_candle(self,candle:Candle) -> Candle:
        try:
            self._logger.debug(f"Add Candle to:{candle.asset}")

            if candle.asset in self.assets:
                self.assets[candle.asset].add_candle(candle)
                self._add_candle_to_db(candle)
                return candle
        except Exception as e:
            self._logger.exception("Failed to add candle to db with exception {}".format(e))

    def add_relation(self, relation: Relation)->bool:
        try:
            if relation.asset in self.assets:
                self.assets[relation.asset].add_relation(relation)
                return True
            return False
        except Exception as e:
            self._logger.exception("Failed to add relation to asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def update_relation(self,relation:Relation):
        try:
            if relation.asset in self.assets:
                self.assets[relation.asset].update_relation(relation)
        except Exception as e:
            self._logger.exception("Failed to update relation for asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def remove_relation(self,relation:Relation):
        try:
            if relation.asset in self.assets:
                self.assets[relation.asset].remove_relation(relation)
        except Exception as e:
            self._logger.exception("Failed to remove relation from asset {asset},Error:{e}".format(asset=relation.asset, e=e))

    def add_candles_series(self,asset:str,maxlen:int,timeframe:int,broker:str):
        try:
            if asset in self.assets:
                self.assets[asset].add_candles_series(maxlen,timeframe,broker)
        except Exception as e:
            self._logger.exception("Failed to add candles series to asset {asset},Error:{e}".format(asset=asset, e=e))

    def add_smt_pair(self, asset: str, smt_pair: SMTPair):
        try:
            if asset in self.assets:
                self.assets[asset].add_smt_pair(smt_pair)
        except Exception as e:
            self._logger.exception("Failed to add smt pair to asset {asset},Error:{e}".format(asset=asset, e=e))

    # endregion

    # region Return Functions

    def return_asset_class(self, asset: str) -> str:
        try:
            if asset in self.assets:
                return self.assets[asset].asset_class
        except Exception as e:
            self._logger.exception("Failed to return asset class for asset {asset},Error:{e}".format(asset=asset, e=e))

    def return_relations(self, asset: str,broker:str) -> list[Relation]:
        try:
            if asset in self.assets:
                return self.assets[asset].return_relations(broker)
        except Exception as e:
            self._logger.exception("Failed to return relations for asset:{asset},Error {e}".format(asset=asset, e=e))

    def return_candles(self, asset: str, broker: str, timeFrame: int) -> list[Candle]:
        try:
            if asset in self.assets:
                return self.assets[asset].return_candles(timeFrame, broker)
        except Exception as e:
            self._logger.exception("Failed to return candles for asset {asset},Error {e}".format(asset=asset, e=e))

    def return_all_relations(self, asset: str)->list[Relation]:
        try:
            if asset in self.assets:
                return self.assets[asset].relations
        except Exception as e:
            self._logger.exception("Failed to return relations for asset{asset},Error {e}".format(asset=asset, e=e))
    # endregion
