from app.models.trade.Trade import Trade

class StrategyResult:
    def __init__(self, status:str, trade:Trade):
        self.status:str = status
        self.trade:Trade = trade
