from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.db.mongodb.dtos.RelationDTO import RelationDTO
from app.db.mongodb.dtos.SMTPairDTO import SMTPairDTO
from app.db.mongodb.dtos.StrategyDTO import StrategyDTO
from app.mappers.DTOMapper import DTOMapper
from app.models.asset.Relation import Relation
from app.models.asset.SMTPair import SMTPair


class RelationRepository:

    def __init__(self, db_name:str,uri:str):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = DTOMapper()

    def add_relation(self,relation:Relation):
        asset_dto:AssetDTO = self.find_asset_by_name(relation.asset)
        broker_dto:BrokerDTO = self.find_broker_by_name(relation.broker)
        strategy_dto:StrategyDTO = self.find_strategy_by_name(relation.strategy)

        relations_dtos:list[RelationDTO] = self.find_relations()

        highest_id = max(relations_dtos, key=lambda x: x.relationId).relationId

        relation_dto = RelationDTO(assetId=asset_dto.assetId,brokerId=broker_dto.brokerId
                                   ,strategyId=strategy_dto.strategyId
                                   ,maxTrades=relation.max_trades,relationId=highest_id+1)

        self._db.add("Relation",relation_dto.model_dump(exclude={"id"}))

    def find_relations(self):
        relations_db:list = self._db.find("Relation",None)
        relations:list[RelationDTO] = []
        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_relation_by_id(self,relation_id:int)->RelationDTO:
        query = self._db.buildQuery("relationId", relation_id)
        return RelationDTO(**self._db.find("Relation",query)[0])

    def find_relations_by_asset_id(self,asset_id:int)->list[RelationDTO]:
        query = self._db.buildQuery("assetId", asset_id)

        relations_db:list = self._db.find("Relation",query)

        relations:list[RelationDTO] = []

        for relation in relations_db:
            relations.append(RelationDTO(**relation))
        return relations

    def find_asset_by_id(self,asset_id:int)->AssetDTO:
        query = self._db.buildQuery("assetId", asset_id)
        return AssetDTO(**self._db.find("Asset",query)[0])

    def find_asset_by_name(self,name:str)->AssetDTO:
        query = self._db.buildQuery("name", name)
        return AssetDTO(**self._db.find("Asset",query)[0])

    def find_broker_by_name(self,name:str)->BrokerDTO:
        query = self._db.buildQuery("name", name)
        return BrokerDTO(**self._db.find("Broker",query)[0])

    def find_strategy_by_name(self,name:str)->StrategyDTO:
        query = self._db.buildQuery("name", name)
        return StrategyDTO(**self._db.find("Strategy",query)[0])

    def find_broker_by_id(self,_id:int)->BrokerDTO:
        query = self._db.buildQuery("brokerId", _id)
        return BrokerDTO(**self._db.find("Broker",query)[0])

    def find_strategy_by_id(self,_id:int)->StrategyDTO:
        query = self._db.buildQuery("strategyId", _id)
        return StrategyDTO(**self._db.find("Strategy",query)[0])

    def update_relation(self,relation:Relation):
        dto:RelationDTO = self.find_relation_by_id(relation.id)

        asset_dto:AssetDTO = self.find_asset_by_name(relation.asset)
        broker_dto:BrokerDTO = self.find_broker_by_name(relation.broker)
        strategy_dto:StrategyDTO = self.find_strategy_by_name(relation.strategy)

        relation_dto = RelationDTO(assetId=asset_dto.assetId,brokerId=broker_dto.brokerId
                                   ,maxTrades=relation.max_trades,relationId=dto.relationId,strategyId=strategy_dto.strategyId)

        self._db.update("Relation",dto.id,relation_dto.model_dump(exclude={"id"}))

    def delete_relation(self,relation:Relation):
        dto:RelationDTO = self.find_relation_by_id(relation.id)

        self._db.delete("Relation",dto.id)

    def add_smt_pair(self,smt_pair:SMTPair):
        strategy_dto = self.find_strategy_by_name(smt_pair.strategy)
        asset_a_dto = self.find_asset_by_name(smt_pair.asset_a)
        asset_b_dto = self.find_asset_by_name(smt_pair.asset_b)

        dto = SMTPairDTO(strategyId=strategy_dto.strategyId,assetAId=asset_a_dto.assetId,assetBId=asset_b_dto.assetId
                         ,correlation=smt_pair.correlation)

        self._db.add("SMTPairs",dto.model_dump(exclude={"id"}))

    def find_smt_pairs(self)->list[SMTPairDTO]:
        smt_pairs_db:list = self._db.find("SMTPairs",None)
        smt_pairs:list[SMTPairDTO] = []
        for smt_pair in smt_pairs_db:
            smt_pairs.append(SMTPairDTO(**smt_pair))
        return smt_pairs

    def find_smt_pair_by_smt_pair(self,smt_pair:SMTPair)->SMTPairDTO:
        strategy_dto = self.find_strategy_by_name(smt_pair.strategy)
        asset_a_dto = self.find_asset_by_name(smt_pair.asset_a)
        asset_b_dto = self.find_asset_by_name(smt_pair.asset_b)

        query = { "strategyId": strategy_dto.strategyId, "assetAId": asset_a_dto.assetId
            , "assetBId": asset_b_dto.assetId, "correlation": smt_pair.correlation }

        smt_pair_db:list = self._db.find("SMTPairs",query)
        smt_pair_dto:SMTPairDTO = SMTPairDTO(**smt_pair_db[0])
        return smt_pair_dto

    def delete_smt_pair(self,smt_pair:SMTPair):
        dto = self.find_smt_pair_by_smt_pair(smt_pair)

        self._db.delete("SMTPairs",dto.id)
