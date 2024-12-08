from dataclasses import dataclass, field
from typing import Optional

from Models.API.GETParams import GETParams


# GET /v5/order/realtime
# Primarily query unfilled or partially filled orders in real-time,
# but also supports querying recent 500 closed status (Cancelled, Filled)
# orders.
@dataclass
class OpenAndClosedOrders(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    openOnly: Optional[int] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    limit: Optional[int] = field(default=None)
    cursor: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            return self.validateLinear()
        return False

    def validateLinear(self) -> bool:
        if self.category == "linear":
            if self.baseCoin is not None or self.settleCoin is not None or self.settleCoin is not None:
                return True
            return False
        return True

