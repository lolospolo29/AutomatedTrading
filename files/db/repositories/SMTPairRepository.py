from files.db.MongoDB import MongoDB
from files.models.asset.SMTPair import SMTPair

class SMTPairRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region SMT

    def add_smt_pair(self, smt_pair: SMTPair):
        self._db.add("SMTPairs", smt_pair.model_dump(exclude={"id"}))

    def find_smt_pairs(self) -> list[SMTPair]:
        smt_pairs_db: list = self._db.find("SMTPairs", None)
        smt_pairs: list[SMTPair] = []
        for smt_pair in smt_pairs_db:
            smt_pairs.append(SMTPair(**smt_pair))
        return smt_pairs

    def find_smt_pair_by_id(self, smt_pair_id: int) -> SMTPair:
        query = self._db.build_query("smtPairId", smt_pair_id)
        return SMTPair(**self._db.find("Relation", query)[0])

    def update_relation(self, smt_pair: SMTPair):
        dto: SMTPair = self.find_smt_pair_by_id(smt_pair.smt_pair_id)

        self._db.update("Relation", dto.id, dto.model_dump(exclude={"id"}))

    def delete_smt_pair(self, smt_pair: SMTPair):
        dto: SMTPair = self.find_smt_pair_by_id(smt_pair.smt_pair_id)

        self._db.delete("SMTPairs", dto.id)

    # endregion