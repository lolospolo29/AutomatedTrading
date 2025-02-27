from abc import abstractmethod

from app.helper.handler.SMTHandler import SMTHandler
from app.models.asset.Relation import Relation
from app.models.strategy.Strategy import Strategy
from app.models.trade.Trade import Trade
from app.models.strategy.StrategyResult import StrategyResult


class SMTStrategy(Strategy):

    @abstractmethod
    def is_in_time(self, time) -> bool:
        pass
    @abstractmethod
    def get_entry(self, candles: list, timeFrame: int, relation: Relation, asset_class: str) -> StrategyResult:
        pass
    @abstractmethod
    def get_exit(self, candles: list, timeFrame: int, trade: Trade, relation: Relation) -> StrategyResult:
        pass
