from files.db.mongodb.MongoDB import MongoDB
from files.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from files.db.mongodb.dtos.AssetDTO import AssetDTO
from files.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from files.mappers.DTOMapper import DTOMapper
from files.models.asset.Asset import Asset

class AssetRepository:

    def __init__(self, db_name:str,uri:str,dto_mapper:DTOMapper):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = dto_mapper

    # region Asset Class CRUD

    def find_asset_class_by_name(self,name:str)->AssetClassDTO:
        query = self._db.buildQuery("name", name)

        return AssetClassDTO(**self._db.find("AssetClasses",query)[0])

    def find_asset_class_by_id(self,_id:int)->AssetClassDTO:
        query = self._db.buildQuery("assetClassId", _id)
        return AssetClassDTO(**self._db.find("AssetClasses",query)[0])

    def find_asset_classes(self):
        asset_classes_db: list = self._db.find("AssetClasses", None)

        asset_classes:list[AssetClassDTO] = []

        for asset_class in asset_classes_db:
            asset_classes.append(AssetClassDTO(**asset_class))

        return asset_classes
    # endregion

    # region Asset CRUD

    def find_assets(self)->list[AssetDTO]:
        assets_db: list = self._db.find("Asset", None)

        assets:list[AssetDTO] = []

        for asset in assets_db:
            assets.append(AssetDTO(**asset))

        return assets

    def find_asset_by_id(self,asset_id:int)->AssetDTO:
        query = self._db.buildQuery("assetId", asset_id)
        return AssetDTO(**self._db.find("Asset",query)[0])

    def add_asset(self,asset:Asset):
        assetClass:AssetClassDTO = self.find_asset_class_by_name(asset.asset_class)

        assets_dtos:list[AssetDTO] = self.find_assets()

        highest_id = max(assets_dtos, key=lambda x: x.assetId).assetId

        dto:AssetDTO = self._dto_mapper.map_asset_to_dto(asset,assetClass.assetClassId,highest_id+1)

        self._db.add("Asset",dto.model_dump())

    def delete_asset(self,asset:Asset):
        dto:AssetDTO = self.find_asset_by_id(asset.asset_id)

        self._db.delete("Asset",dto.id)

    def update_asset(self,asset:Asset):
        assetClass:AssetClassDTO = self.find_asset_class_by_name(asset.asset_class)

        asset_dto = self.find_asset_by_id(asset.asset_id)

        dto = self._dto_mapper.map_asset_to_dto(asset=asset,asset_id=asset.asset_id,asset_class_id=assetClass.assetClassId)

        self._db.update("Asset",asset_dto.id,dto.model_dump())
    # endregion

    def find_smt_pair_by_id(self,strategyId:int=None,assetAId:int=None,assetBId:int=None)->list[SMTPairDTO]:
        if strategyId is None and assetAId is None and assetBId is None:
            return []
        # Build the query dynamically, excluding None values
        query = {k: v for k, v in {
            "strategyId": strategyId,
            "assetAId": assetAId,
            "assetBId": assetBId
        }.items() if v is not None}

        smt_pairs: list[SMTPairDTO] = []
        smt_pairs_db: list = self._db.find("SMTPairs", query)

        for smt_pair in smt_pairs_db:
            smt_pairs.append(SMTPairDTO(**smt_pair))

        return smt_pairs
