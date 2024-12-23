from dataclasses import dataclass, field
from typing import Optional

from app.API.POSTParams import POSTParams


# POST /v5/order/cancel-all
@dataclass
class CancelAllOrders(POSTParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    stopOrderType: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if self.category and self.validateCoin():
            return True
        return False

    def validateCoin(self) -> bool:
        if self.category == "linear" or self.category == "inverse":
            if self.baseCoin:
                return True
            if self.symbol:
                return True
            if self.settleCoin:
                return True
            return False

