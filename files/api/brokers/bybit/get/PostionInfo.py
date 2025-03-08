from dataclasses import dataclass, field
from typing import Optional

from files.api.GETParams import GETParams


# get /v5/position/list
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
    baseCoin: Optional[str] = field(default=None) # not in order
    settleCoin: Optional[str] = field(default=None) # not in order
    limit: Optional[int] = field(default=None) # not in order max 200
    cursor: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            if self._validateLinear() and self._validateBaseCoin():
                return True
        return False

    def _validateBaseCoin(self) -> bool:
        """Validate base coin parameters."""
        if self.baseCoin:
            if self.category == "option":
                return True
            return False
        return True

    def _validateLinear(self):
        if self.category == "linear":
            if self.settleCoin or self.symbol:
                return True
            return False
        return True