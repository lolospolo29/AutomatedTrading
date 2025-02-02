from app.models.trade.Trade import Trade


class StrategyResult:
    def __init__(self,trade: Trade=None,status:str=None):
        self.trade : Trade = trade
        self.status : str = status
