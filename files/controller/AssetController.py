from logging import Logger
from typing import Dict, Any

from files.models.asset.AssetClass import AssetClass
from files.helper.manager.AssetManager import AssetManager
from files.models.asset.Asset import Asset

class AssetController:

    # region Initializing
    def __init__(self, asset_manager: AssetManager,logger: Logger):
        self._AssetManager = asset_manager
        self._logger = logger

    def create_asset(self, json_data: Dict[str, Any]) -> None:
        try:
            self._AssetManager.create_asset(Asset.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Add Asset failed,Error: {e}".format(e=e))

    def get_assets(self) -> list[dict]:
        assets = self._AssetManager.get_assets()
        dict_assets = []
        for asset in assets:
            try:
                asset_dict: dict = asset.dict(exclude={'candles_series','_id'})
                dict_assets.append(asset_dict)
            except Exception as e:
                self._logger.error(
                    "Error appending asset to list Name: {name},Error:{e}".format(name=asset.name, e=e))
                continue
        return dict_assets

    def get_asset_classes(self):
        asset_classes: list[AssetClass] = self._AssetManager.get_asset_classes()
        dict_asset_classes = []
        for asset_class in asset_classes:
            try:
                asset_class_dict: dict = asset_class.dict(exclude={"_id"})
                dict_asset_classes.append(asset_class_dict)
            except Exception as e:
                self._logger.error("Error while dumping Asset Class,Error:{e}".format(e=e))
                continue
        return dict_asset_classes

    def update_asset(self, json_data: Dict[str, Any]):
        try:
            self._AssetManager.update_asset(Asset.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Update Asset failed,Error: {e}".format(e=e))

    def delete_asset(self, json_data: Dict[str, Any] = None):
        try:
            asset = Asset.model_validate(json_data)
            self._AssetManager.delete_asset(asset)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))