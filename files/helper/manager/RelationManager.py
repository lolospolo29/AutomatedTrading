import threading
from logging import Logger

from files.db.repositories.RelationRepository import RelationRepository
from files.helper.manager.AssetManager import AssetManager
from files.models.asset.Category import Category
from files.models.asset.Relation import Relation

class RelationManager:

    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(RelationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, relation_repository:RelationRepository
                 ,asset_manager:AssetManager,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._lock = threading.Lock()
            self._relations:list[Relation] = []
            self._relation_repository = relation_repository
            self._asset_manager = asset_manager
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    # endregion

    def create_relation(self, relation: Relation):
        try:
            self._logger.info(f"Adding relation to db:{relation}")
            self._relation_repository.add_relation(relation)
            self.add_relation(relation)
        except Exception as e:
            self._logger.exception(f"Failed to add relation:{relation},Exception:{e}")

    def add_relation(self, relation:Relation):
        with self._lock:
            if relation not in self._relations:
                try:
                    self._logger.info(f"Adding relation:{relation}")
                    self._relations.append(relation)
                except Exception as e:
                    self._logger.exception(f"Failed to add relation:{relation},Exception:{e}")

    def get_categories(self)->list[Category]:
        return self._relation_repository.find_categories()

    def get_relation_for_id(self, relation_id:int)->Relation:
        return self._relation_repository.find_relation_by_id(relation_id)

    def get_relations(self)->list[Relation]:
        return self._relation_repository.find_relations()

    def update_relation(self, relation:Relation):
        with self._lock:
            if relation in self._relations:
                try:
                    self._logger.info(f"Updating relation:{relation}")
                    index = self._relations.index(relation)
                    self._relations[index] = relation
                    self._relation_repository.update_relation(relation=relation)
                except Exception as e:
                    self._logger.exception(f"Failed to update relation:{relation},Exception:{e}")

    def remove_relation(self, relation:Relation):
        with self._lock:
            if relation in self._relations:
                self._logger.info(f"Removing relation:{relation}")
                self._relations.remove(relation)

    def delete_relation(self, relation:Relation):
        with self._lock:
            if relation in self._relations:
                try:
                    self._logger.info(f"Deleting relation:{relation}")
                    self._relation_repository.delete_relation(relation=relation)
                    self._relations.remove(relation)
                except Exception as e:
                    self._logger.exception(f"Failed to delete relation:{relation},Exception:{e}")