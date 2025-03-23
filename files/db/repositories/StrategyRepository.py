from files.db.MongoDB import MongoDB
from files.models.strategy.EntryExitstrategyDTO import EntryExitStrategyDTO
from files.models.strategy.StrategyDTO import StrategyDTO


class StrategyRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Strategy

    def add_strategy(self, strategy: StrategyDTO):
        self._db.add("Strategy", strategy.model_dump(exclude={"id"}))

    def find_strategies(self)->list[StrategyDTO]:
        strategies_db: list = self._db.find("Strategy", None)
        strategies: list[StrategyDTO] = []
        for strategy in strategies_db:
            strategies.append(StrategyDTO(**strategy))
        return strategies

    def find_strategy_by_id(self, _id: int) -> StrategyDTO:
        query = self._db.build_query("strategyId", _id)
        return StrategyDTO(**self._db.find("Strategy", query)[0])

    def find_strategy_by_name(self, name: str) -> StrategyDTO:
        query = self._db.build_query("name", name)
        return StrategyDTO(**self._db.find("Strategy", query)[0])

    # endregion

    # region Entry Exit Strategy

    def find_entry_exit_strategy_by_id(self, _id: int) -> EntryExitStrategyDTO:
        query = self._db.build_query("strategyId", _id)
        return EntryExitStrategyDTO(**self._db.find("EntryExitStrategy", query)[0])

    def find_entry_exit_strategies(self) -> list[EntryExitStrategyDTO]:
        strategies_db: list = self._db.find("EntryExitStrategy", None)
        strategies: list[EntryExitStrategyDTO] = []
        for strategy in strategies_db:
            strategies.append(EntryExitStrategyDTO(**strategy))
        return strategies

    # endregion
