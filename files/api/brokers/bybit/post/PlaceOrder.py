from typing import Optional

from pydantic import BaseModel, Field


class PlaceOrder(BaseModel):
    symbol: str
    side: str
    orderType: str
    qty: str

    #Optional Because Batch must be set with Normal Place Order
    category: Optional[str] = Field(default=None)

    # Optional parameters
    isLeverage: Optional[int] = Field(default=None)
    marketUnit: Optional[str] = Field(default=None)
    price: Optional[str] = Field(default=None)
    triggerDirection: Optional[int] = Field(default=None)
    orderFilter: Optional[str] = Field(default=None)
    triggerPrice: Optional[str] = Field(default=None)
    triggerBy: Optional[str] = Field(default=None)
    orderlv: Optional[str] = Field(default=None)
    timeInForce: Optional[str] = Field(default=None)
    positionIdx: Optional[int] = Field(default=None)
    orderLinkId: Optional[str] = Field(default=None)
    takeProfit: Optional[str] = Field(default=None)
    stopLoss: Optional[str] = Field(default=None)
    tpTriggerBy: Optional[str] = Field(default=None)
    slTriggerBy: Optional[str] = Field(default=None)
    reduceOnly: Optional[bool] = Field(default=None)
    closeOnTrigger: Optional[bool] = Field(default=None)
    smpType: Optional[str] = Field(default=None)
    mmp: Optional[bool] = Field(default=None)
    tpslMode: Optional[str] = Field(default=None)
    tpLimitPrice: Optional[str] = Field(default=None)
    slLimitPrice: Optional[str] = Field(default=None)
    tpOrderType: Optional[str] = Field(default=None)
    slOrderType: Optional[str] = Field(default=None)

    def validate(cls) -> bool:
        """Validate required parameters for placing an order."""
        # Check required parameters
        if not (cls.symbol and cls.side and cls.orderType and cls.qty):
            print("Validation Error: 'symbol', 'side', 'orderType', and 'qty' are required.")
            return False
        return True