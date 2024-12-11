from dataclasses import dataclass, field
from typing import Optional

from Core.API.POSTParams import POSTParams


# POST /v5/position/trading-stop
# Set the take profit, stop loss or trailing stop for the position.
@dataclass
class TradingStop(POSTParams):
    # Required parameter
    category: str
    symbol: str

    # Optional parameters
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    trailingStop: Optional[str] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)
    activePrice: Optional[str] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
    tpSize: Optional[str] = field(default=None)
    slSize: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)
    tpOrderType: Optional[str] = field(default=None)
    slOrderType: Optional[str] = field(default=None)
    positionIdx: Optional[int] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category and self.symbol:
            return True
        return False
