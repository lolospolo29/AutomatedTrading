from typing import Optional

from pydantic import BaseModel, Field


# post /v5/order/cancel-all
class CancelAllOrders(BaseModel):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = Field(default=None)
    baseCoin: Optional[str] = Field(default=None)
    settleCoin: Optional[str] = Field(default=None)
    orderFilter: Optional[str] = Field(default=None)
    stopOrderType: Optional[str] = Field(default=None)

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

