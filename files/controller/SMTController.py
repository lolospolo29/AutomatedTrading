from logging import Logger
from typing import Dict, Any

from files.helper.manager.SMTManager import SMTManager
from files.models.asset.SMTPair import SMTPair

class SMTController:

    def __init__(self,logger:Logger, smt_manager:SMTManager):
        self._SMT_manager = smt_manager
        self._logger = logger

    def create_smt_pair(self, json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._SMT_manager.create_smt(smt_pair)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_smt_pairs(self)->list[dict]:
        smt_pairs:list[SMTPair] = self._SMT_manager.return_smt_pairs()
        dict_smt_pairs = []
        for smt_pair in smt_pairs:
            try:
                relation_dict:dict = smt_pair.dict(exclude={'_id'})
                dict_smt_pairs.append(relation_dict)
            except Exception as e:
                self._logger.error("Error appending relation to list: {id},Error:{e}".format(id=smt_pair.strategy,e=e))
                continue
        return dict_smt_pairs

    def delete_smt_pair(self, json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._SMT_manager.delete_smt(smt_pair)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))