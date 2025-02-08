from typing import Optional

from app.models.trade.Trade import Trade


class StrategyResult:
    def __init__(self, trade: Optional[Trade] = None, status: Optional[str] = None):
        self.trade: Optional[Trade] = trade
        self.status: Optional[str] = status
