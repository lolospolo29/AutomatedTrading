from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade


class StrategyResult:
    def __init__(self,trade: Trade):
        self.trade : Trade = trade
        self.orders:dict[Order,StrategyResultStatusEnum] = {}
