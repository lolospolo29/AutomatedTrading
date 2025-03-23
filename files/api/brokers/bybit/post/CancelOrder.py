from typing import Optional

from pydantic import BaseModel, Field

# post /v5/order/cancel
# You can only cancel unfilled or partially filled orders.
class CancelOrder(BaseModel):
    # Required parameter
    category: str
    symbol: str

    # Either one Required
    orderId: Optional[str] = Field(default=None)
    orderLinkId: Optional[str] = Field(default=None)

    # Optional parameters
    orderFilter: Optional[str] = Field(default=None)

    def validate(self):
        """Validate required parameters."""
        if self.category and self.symbol and (self.orderId or self.orderLinkId):
            return True
        return False
