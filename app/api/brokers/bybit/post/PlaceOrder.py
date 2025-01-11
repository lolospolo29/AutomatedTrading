from dataclasses import dataclass, field
from typing import Optional

from app.api.POSTParams import POSTParams


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

        # Validate `category` if batchOrder is False
        if not self.category:
            print("Validation Error: 'category' is required")
            return False

        # Validate `orderType`
        valid_order_types = {"Limit", "Market", "Stop", "StopLimit", "LimitIfTouched", "MarketIfTouched"}
        if self.orderType not in valid_order_types:
            print(f"Validation Error: Invalid 'orderType'. Must be one of {valid_order_types}.")
            return False

        # Validate `timeInForce` for Limit orders
        if self.orderType == "Limit" and not self.timeInForce:
            print("Validation Error: 'timeInForce' is required for 'Limit' orders.")
            return False

        # Validate trigger-related fields for conditional orders
        if self.orderType in {"Stop", "StopLimit", "LimitIfTouched", "MarketIfTouched"}:
            if not self.triggerPrice:
                print("Validation Error: 'triggerPrice' is required for conditional orders.")
                return False
            if self.triggerDirection not in {1, 2}:
                print("Validation Error: 'triggerDirection' must be 1 (up) or 2 (down) for conditional orders.")
                return False

        # Validate `takeProfit` and `stopLoss`
        if self.takeProfit and not self.tpTriggerBy:
            print("Validation Error: 'tpTriggerBy' is required if 'takeProfit' is provided.")
            return False
        if self.stopLoss and not self.slTriggerBy:
            print("Validation Error: 'slTriggerBy' is required if 'stopLoss' is provided.")
            return False

        # Validate `reduceOnly` and `closeOnTrigger`
        if self.reduceOnly and self.closeOnTrigger:
            print("Validation Error: 'reduceOnly' and 'closeOnTrigger' cannot both be True.")
            return False

        # Additional validation can be added here as needed

        # If all checks pass
        return True

