from files.db.MongoDB import MongoDB
from files.models.asset.Asset import Asset
from files.models.asset.AssetClass import AssetClass

class AssetRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Asset Class

    def find_asset_classes(self):
        query = {}

        asset_classes_db: list = self._db.find("AssetClasses", query)

        asset_classes:list[AssetClass] = []

        for asset_class in asset_classes_db:
            asset_classes.append(AssetClass(**asset_class))

        return asset_classes

    def find_asset_class_by_name(self,name:str)->AssetClass:
        query = self._db.build_query("name", name)

        return AssetClass(**self._db.find("AssetClasses", query)[0])

    def find_asset_class_by_id(self,_id:int)->AssetClass:
        query = self._db.build_query("assetClassId", _id)
        return AssetClass(**self._db.find("AssetClasses", query)[0])

    # endregion

    # region Asset

    def add_asset(self, asset:Asset):
        self._db.add("Asset",asset.model_dump(exclude={"id"}))

    def find_asset_by_id(self,asset_id:int)->Asset:
        query = self._db.build_query("assetId", asset_id)
        return Asset(**self._db.find("Asset", query)[0])

    def find_assets(self)->list[Asset]:
        query = {}

        assets_db: list = self._db.find("Asset", query)

        assets:list[Asset] = []

        for asset in assets_db:
            assets.append(Asset(**asset))

        return assets

    def update_asset(self, asset:Asset):
        dto:Asset = self.find_asset_by_id(asset.asset_id)

        self._db.update("Asset",str(dto.id),asset.model_dump(exclude={"id"}))

    def delete_asset(self, asset:Asset):
        dto:Asset = self.find_asset_by_id(asset.asset_id)

        self._db.delete("Asset",str(dto.id))

    # endregion