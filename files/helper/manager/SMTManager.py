import threading
from logging import Logger

from files.db.repositories.AssetRepository import AssetRepository
from files.db.repositories.RelationRepository import RelationRepository
from files.models.asset.SMTPair import SMTPair
from files.helper.manager.AssetManager import AssetManager
from files.models.asset.SMTPair import SMTPair

class SMTManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(SMTManager, cls).__new__(cls)
        return cls._instance

    def __init__(self,logger:Logger,relation_repository:RelationRepository,asset_repository:AssetRepository,asset_manager:AssetManager):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._relation_repository = relation_repository
            self._asset_repository = asset_repository
            self._asset_manager = asset_manager
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    def add_smt(self, smt_pair:SMTPair):
        self._logger.info(f"Adding SMT,{smt_pair.asset_a},{smt_pair.asset_b},{smt_pair.correlation} to db and manager.")
        self._asset_manager.add_smt_pair(asset=smt_pair.asset_a,smt_pair=smt_pair)
        self._asset_manager.add_smt_pair(asset=smt_pair.asset_b,smt_pair=smt_pair)

    def create_smt(self, smt_pair:SMTPair):
        self._logger.info(f"Adding SMT,{smt_pair.asset_a},{smt_pair.asset_b},{smt_pair.correlation} to db and manager.")
        self._relation_repository.add_smt_pair(smt_pair=smt_pair)
        self.add_smt(smt_pair=smt_pair)

    def return_smt_pairs(self)->list[SMTPair]:
        smt_pair_dtos:list[SMTPair] = self._relation_repository.find_smt_pairs()

        smt_pairs:list[SMTPair] = []

        for smt_pair_dto in smt_pair_dtos:
            try:
                smt_pair_dto:SMTPair = smt_pair_dto

                asset_a_dto = self._asset_repository.find_asset_by_id(smt_pair_dto.asset_a_id)
                asset_b_dto = self._asset_repository.find_asset_by_id(smt_pair_dto.asset_b_id)
                strategy_dto = self._relation_repository.find_strategy_by_id(smt_pair_dto.strategy_id)

                smt_pair = SMTPair(strategy=strategy_dto.name, asset_a=asset_a_dto.name, asset_b=asset_b_dto.name
                                   , correlation=smt_pair_dto.correlation)

                smt_pairs.append(smt_pair)
            except Exception as e:
                self._logger.critical("Failed to add SMT pair to db and manager. Error:{e}".format(e=e))
                continue
        return smt_pairs

    def delete_smt(self, smt_pair:SMTPair):
        self._relation_repository.delete_smt_pair(smt_pair=smt_pair)
