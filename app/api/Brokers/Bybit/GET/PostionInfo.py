from dataclasses import dataclass, field
from typing import Optional

from app.API.GETParams import GETParams


# GET /v5/position/list
# Query real-time position data,
# such as position size, cumulative realizedPNL.
# symbol parameter is supported to be passed with multiple symbols
# up to 10, e.g., "symbol=BTCUSD,ETHUSD"
@dataclass
class PositionInfo(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    limit: Optional[str] = field(default=None)
    cursor: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            if self.validateLinear() and self.validateBaseCoin():
                return True
        return False

    def validateBaseCoin(self) -> bool:
        """Validate base coin parameters."""
        if self.baseCoin:
            if self.category == "option":
                return True
            return False
        return True

    def validateLinear(self):
        if self.category == "linear":
            if self.settleCoin or self.symbol:
                return True
            return False
        return True