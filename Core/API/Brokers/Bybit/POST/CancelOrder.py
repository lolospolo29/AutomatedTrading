from dataclasses import dataclass, field
from typing import Optional

from Core.API.POSTParams import POSTParams


# POST /v5/order/cancel
# You can only cancel unfilled or partially filled orders.
@dataclass
class CancelOrder(POSTParams):
    # Required parameter
    category: str
    symbol: str

    # Either one Required
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)

    # Optional parameters
    orderFilter: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if self.category and self.symbol and (self.orderId or self.orderLinkId):
            return True
        return False
