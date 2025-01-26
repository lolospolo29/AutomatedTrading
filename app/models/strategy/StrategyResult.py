from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Trade import Trade


class StrategyResult:
    def __init__(self,trade: Trade):
        self.trade : Trade = trade
        self.status : StrategyResultStatusEnum = StrategyResultStatusEnum.NONEW
