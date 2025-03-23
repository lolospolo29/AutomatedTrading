from typing import Optional

from pydantic import BaseModel, Field

# post /v5/order/amend
# You can only modify unfilled or partially filled orders.
class AmendOrder(BaseModel):
    # Required parameter
    category: str
    symbol: str

    # Either one Required
    orderId: Optional[str] = Field(default=None)
    orderLinkId: Optional[str] = Field(default=None)

    # Optional parameters
    orderlv: Optional[str] = Field(default=None)
    triggerPrice: Optional[str] = Field(default=None)
    price: Optional[str] = Field(default=None)
    tpslMode: Optional[str] = Field(default=None)
    takeProfit: Optional[str] = Field(default=None)
    stopLoss: Optional[str] = Field(default=None)
    tpTriggerBy: Optional[str] = Field(default=None)
    slTriggerBy: Optional[str] = Field(default=None)
    triggerBy: Optional[str] = Field(default=None)
    tpLimitPrice: Optional[str] = Field(default=None)
    slLimitPrice: Optional[str] = Field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if  (self.category and self.symbol and (self.orderId or self.orderLinkId) and self._validateOrderlv() and
                self._validateTPSL()):
            return True
        return False

    def _validateOrderlv(self) -> bool:
        if self.orderlv:
            if self.category == "option":
                return True
            return False
        return True
    def _validateTPSL(self) -> bool:
        if self.takeProfit:
            if self.tpTriggerBy:
                return True
            return False
        if self.stopLoss:
            if self.slTriggerBy:
                return True
            return False
        return True