from dataclasses import dataclass, field
from typing import Optional

from app.api.GETParams import GETParams


# get /v5/order/realtime
# Primarily query unfilled or partially filled orders in real-time,
# but also supports querying recent 500 closed status (Cancelled, Filled)
# orders.
@dataclass
class OpenAndClosedOrders(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None) # not in order
    settleCoin: Optional[str] = field(default=None) # not in order
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    openOnly: Optional[int] = field(default=None) # open Only
    orderFilter: Optional[str] = field(default=None) # exits but different enums
    limit: Optional[int] = field(default=None) # page size receiving
    cursor: Optional[str] = field(default=None) # safe for next page

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            return True
        return False


