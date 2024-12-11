from dataclasses import dataclass, field
from typing import Optional

from Core.API.POSTParams import POSTParams


# POST /v5/order/amend
# You can only modify unfilled or partially filled orders.
@dataclass
class AmendOrder(POSTParams):
    # Required parameter
    category: str
    symbol: str

    # Either one Required
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)

    # Optional parameters
    orderlv: Optional[str] = field(default=None)
    triggerPrice: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)
    triggerBy: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if  self.category and self.symbol and (self.orderId or self.orderLinkId) and self.validateOrderlv():
            return True
        return False

    def validateOrderlv(self) -> bool:
        if self.orderlv:
            if self.category == "option":
                return True
            return False
        return True
