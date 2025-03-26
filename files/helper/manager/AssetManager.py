import threading
from logging import Logger

from files.db.repositories.AssetRepository import AssetRepository
from files.db.repositories.CandleRepository import CandleRepository
from files.models.asset.AssetClass import AssetClass
from files.models.asset.Asset import Asset
from files.models.asset.Candle import Candle


class AssetManager:
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(AssetManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, asset_respository:AssetRepository, trading_data_repository:CandleRepository, logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.assets: dict[str,Asset] = {}
            self._asset_respository = asset_respository
            self._data_repository = trading_data_repository
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def create_asset(self, asset:Asset):
        try:
            if not asset.name in self.assets:
                self._logger.info("Adding Asset {}".format(asset.name))
                self._asset_respository.add_asset(asset)
        except Exception as e:
            self._logger.critical("Failed to add Asset to db with exception {}".format(e))

    def add_asset(self, asset: Asset) :
        with self._lock:
            if not asset.name in self.assets:
                self.assets[asset.name] = asset
                self._logger.info("Registered asset {}".format(asset.name))

    def add_candle(self,candle:Candle) -> Candle:
        with self._lock:
            try:
                self._logger.debug(f"Add Candle to:{candle.asset}")
                if candle.asset in self.assets:
                    self.assets[candle.asset].add_candle(candle)
                    self._data_repository.add_candle(candle.asset, candle)
                    return candle
            except Exception as e:
                self._logger.exception("Failed to add candle to db with exception {}".format(e))

    def get_assets(self)->list[Asset]:
        return  self._asset_respository.find_assets()

    def get_asset_class(self, asset: str) -> str:
        try:
            if asset in self.assets:
                return self.assets[asset].asset_class
        except Exception as e:
            self._logger.exception("Failed to return asset class for asset {asset},Error:{e}".format(asset=asset, e=e))

    def get_asset_classes(self)->list[AssetClass]:
        return self._asset_respository.find_asset_classes()

    def get_candles(self, asset: str, broker: str, time_frame: int) -> list[Candle]:
        try:
            if asset in self.assets:
                return self.assets[asset].return_candles(time_frame, broker)
        except Exception as e:
            self._logger.exception("Failed to return candles for asset {asset},Error {e}".format(asset=asset, e=e))

    def update_asset(self, asset:Asset):
        with self._lock:
            try:
                dto:Asset = self._asset_respository.find_asset_by_id(asset.asset_id)
                if dto.name in self.assets:
                    self._logger.debug(f"Update Asset:{asset}")
                    self._asset_respository.update_asset(asset)
                    self.assets[asset.name].update_strategy(asset)
            except Exception as e:
                self._logger.critical("Failed to update Asset with exception {}".format(e))

    def remove_asset(self, asset:Asset):
        with self._lock:
            if asset in self.assets:
                self._logger.debug(f"Removing Asset:{asset}")
                del self.assets[asset]

    def delete_asset(self, asset:Asset):
        with self._lock:
            try:
                if asset.name in self.assets:
                    self._logger.debug(f"Delete Asset:{asset}")
                    del self.assets[asset.name]
                    self._asset_respository.delete_asset(asset)
            except Exception as e:
                self._logger.critical("Failed to delete Asset from db with exception {}".format(e))