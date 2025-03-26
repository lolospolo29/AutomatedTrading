import threading
from logging import Logger

from files.db.repositories.SMTPairRepository import SMTPairRepository
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

    def __init__(self,logger:Logger,smt_repository:SMTPairRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._logger = logger
            self._smt_repository = smt_repository
            self._smt_pairs:list[SMTPair] = []
            self._initialized = True  # Markiere als initialisiert

    def create_smt(self, smt_pair:SMTPair):
        self._logger.info(f"Adding SMT,{smt_pair.asset_a},{smt_pair.asset_b},{smt_pair.correlation} to db and manager.")
        self._smt_repository.add_smt_pair(smt_pair)
        self.add_smt(smt_pair)

    def add_smt(self, smt_pair:SMTPair):
        with self._lock:
            self._smt_pairs.append(smt_pair)

    def return_smt_pairs(self)->list[SMTPair]:
        return self._smt_repository.find_smt_pairs()

    def return_smt_pair_by_asset_(self,asset:str)->list[SMTPair]:
        smt_pairs = []
        for smt_pair in self._smt_repository.find_smt_pairs():
            smt_pair:SMTPair
            if (asset==smt_pair.asset_a_id or asset==smt_pair.asset_b_id) and smt_pair not in smt_pairs:
                smt_pairs.append(smt_pair)
        return smt_pairs

    def remove_smt_pair(self, smt_pair: SMTPair):
        with self._lock:
            self._smt_pairs.remove(smt_pair)

    def delete_smt(self, smt_pair:SMTPair):
        self._smt_repository.delete_smt_pair(smt_pair=smt_pair)
        self.remove_smt_pair(smt_pair=smt_pair)