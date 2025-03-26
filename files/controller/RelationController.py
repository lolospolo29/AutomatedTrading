from logging import Logger
from typing import Dict, Any

from files.helper.manager.RelationManager import RelationManager
from files.models.asset.Category import Category
from files.models.asset.Relation import Relation

class RelationController:

    # region Initializing
    def __init__(self
                 , relation_manager:RelationManager, logger:Logger):
        self._Relation_manager = relation_manager
        self._logger = logger
    # endregion

    def create_relation(self, json_data:Dict[str,Any] = None):
        try:
            relation = Relation.model_validate(json_data)
            self._Relation_manager.create_relation(relation=relation)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_relations(self)->list[dict]:
        relations:list[Relation] = self._Relation_manager.get_relations()
        dict_relations = []
        for relation in relations:
            try:
                relation_dict:dict = relation.dict(exclude={"_id"})
                dict_relations.append(relation_dict)
            except Exception as e:
                self._logger.error("Error appending relation to list: {id},Error:{e}".format(id=relation.strategy_id, e=e))
                continue
        return dict_relations

    def get_categories(self):
        categories:list[Category] = self._Relation_manager.get_categories()
        dict_categories = []
        for category in categories:
            try:
                category_dict:dict = category.dict(exclude={"_id"})
                dict_categories.append(category_dict)
            except Exception as e:
                self._logger.error("Error while dumping category name: {name},Error:{e}".format(name=category.name, e=e))
                continue
        return dict_categories

    def update_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.update_relation(Relation.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Update Relation failed,Error: {e}".format(e=e))

    def delete_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.delete_relation(Relation.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Delete Relation failed,Error: {e}".format(e=e))