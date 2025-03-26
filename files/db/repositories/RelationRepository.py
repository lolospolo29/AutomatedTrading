from files.db.MongoDB import MongoDB
from files.models.asset.Asset import Asset
from files.models.trade.Broker import Broker
from files.models.asset.Category import Category
from files.models.asset.Relation import Relation
from files.models.strategy.StrategyDTO import StrategyDTO


class RelationRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Relation

    def add_relation(self, relation: Relation):
        self._db.add("Relation", relation.model_dump(exclude={"_id"}))

    def find_relations(self):
        relations_db: list = self._db.find("Relation", None)
        relations: list[Relation] = []
        for relation in relations_db:
            relations.append(Relation(**relation))
        return relations

    def find_relation_by_id(self, relation_id: int) -> Relation:
        query = self._db.build_query("relationId", relation_id)
        return Relation(**self._db.find("Relation", query)[0])

    def find_relations_by_asset_id(self, asset_id: int) -> list[Relation]:
        query = self._db.build_query("assetId", asset_id)

        relations_db: list = self._db.find("Relation", query)

        relations: list[Relation] = []

        for relation in relations_db:
            relations.append(Relation(**relation))
        return relations

    def update_relation(self, relation: Relation):
        dto: Relation = self.find_relation_by_id(relation.relation_id)

        self._db.update("Relation", dto.id, relation.model_dump(exclude={"_id"}))

    def delete_relation(self, relation: Relation):
        dto: Relation = self.find_relation_by_id(relation.relation_id)

        self._db.delete("Relation", dto.id)

    # endregion

    # region Asset

    def find_asset_by_id(self, asset_id: int) -> Asset:
        query = self._db.build_query("assetId", asset_id)
        return Asset(**self._db.find("Asset", query)[0])

    def find_asset_by_name(self, name: str) -> Asset:
        query = self._db.build_query("name", name)
        return Asset(**self._db.find("Asset", query)[0])

    # endregion

    # region Broker

    def find_broker_by_name(self, name: str) -> Broker:
        query = self._db.build_query("name", name)
        return Broker(**self._db.find("Broker", query)[0])

    def find_broker_by_id(self, id: int) -> Broker:
        query = self._db.build_query("brokerId", id)
        return Broker(**self._db.find("Broker", query)[0])

    # endregion

    # region Strategy

    def find_strategy_by_name(self, name: str) -> StrategyDTO:
        query = self._db.build_query("name", name)
        return StrategyDTO(**self._db.find("Strategy", query)[0])

    def find_strategy_by_id(self, id: int) -> StrategyDTO:
        query = self._db.build_query("strategyId", id)
        return StrategyDTO(**self._db.find("Strategy", query)[0])

    def find_strategies(self) -> list[StrategyDTO]:
        strategies_db: list = self._db.find("Strategy", None)

        strategies: list[StrategyDTO] = []
        for strategy in strategies_db:
            strategies.append(StrategyDTO(**strategy))
        return strategies

    # endregion

    # region Category

    def find_categories(self) -> list[Category]:
        categories_db: list = self._db.find("Category", None)
        categories: list[Category] = []
        for category in categories_db:
            categories.append(Category(**category))
        return categories

    def find_category_by_name(self, name: str) -> Category:
        query = self._db.build_query("name", name)
        return Category(**self._db.find("Category", query)[0])

    def find_category_by_id(self, _id: int) -> Category:
        query = self._db.build_query("categoryId", _id)
        return Category(**self._db.find("Category", query)[0])

    # endregion