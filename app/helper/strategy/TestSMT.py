from app.models.asset.Relation import Relation
from app.models.strategy.SMTStrategy import SMTStrategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class TestSMTStrategy(SMTStrategy):

    def get_exit(self, candles: list, timeFrame: int, trade: Trade, relation: Relation) -> StrategyResult:
        pass

    def get_entry(self, candles: list, timeFrame: int, relation: Relation, asset_class: str) -> StrategyResult:
        pass

    def is_in_time(self, time) -> bool:
        pass