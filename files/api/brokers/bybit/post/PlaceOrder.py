from dataclasses import dataclass, field
from typing import Optional

from files.api.POSTParams import POSTParams


# post /v5/order/create
@dataclass
class PlaceOrder(POSTParams):
    # Required parameter
    symbol: str
    side: str
    orderType: str
    qty: str

    #Optional Because Batch must be set with Normal Place Order
    category: Optional[str] = field(default=None)

    # Optional parameters
    isLeverage: Optional[int] = field(default=None)
    marketUnit: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)
    triggerDirection: Optional[int] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    triggerPrice: Optional[str] = field(default=None)
    triggerBy: Optional[str] = field(default=None)
    orderlv: Optional[str] = field(default=None)
    timeInForce: Optional[str] = field(default=None)
    positionIdx: Optional[int] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)
    reduceOnly: Optional[bool] = field(default=None)
    closeOnTrigger: Optional[bool] = field(default=None)
    smpType: Optional[str] = field(default=None)
    mmp: Optional[bool] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)
    tpOrderType: Optional[str] = field(default=None)
    slOrderType: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters for placing an order."""
        # Check required parameters
        if not (self.symbol and self.side and self.orderType and self.qty):
            print("Validation Error: 'symbol', 'side', 'orderType', and 'qty' are required.")
            return False
        return True
