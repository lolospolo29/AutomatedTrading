from typing import Optional

from pydantic import BaseModel, Field


# get /v5/order/realtime
# Primarily query unfilled or partially filled orders in real-time,
# but also supports querying recent 500 closed status (Cancelled, Filled)
# orders.
class OpenAndClosedOrders(BaseModel):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = Field(default=None)
    baseCoin: Optional[str] = Field(default=None) # not in order
    settleCoin: Optional[str] = Field(default=None) # not in order
    orderId: Optional[str] = Field(default=None)
    orderLinkId: Optional[str] = Field(default=None)
    openOnly: Optional[int] = Field(default=None) # open Only
    orderFilter: Optional[str] = Field(default=None) # exits but different enums
    limit: Optional[int] = Field(default=None) # page size receiving
    cursor: Optional[str] = Field(default=None) # safe for next page

    def validate(self) -> bool:
        """Validate required parameters based on category and other conditions."""
        # Check if category is provided
        if not self.category:
            print("Validation Error: 'category' is required.")
            return False

        # Validate based on category
        if self.category == "linear":
            # For 'linear', at least one of 'symbol', 'baseCoin', or 'settleCoin' must be provided
            if not (self.symbol or self.baseCoin or self.settleCoin):
                print(
                    "Validation Error: For 'linear' category, at least one of 'symbol', 'baseCoin', or 'settleCoin' must be provided.")
                return False

        elif self.category == "inverse":
            # For 'inverse', 'symbol' is required
            if not self.symbol:
                print("Validation Error: For 'inverse' category, 'symbol' is required.")
                return False

        elif self.category == "option":
            # For 'option', 'baseCoin' is required
            if not self.baseCoin:
                print("Validation Error: For 'option' category, 'baseCoin' is required.")
                return False

        elif self.category == "spot":
            # For 'spot', 'symbol' is required
            if not self.symbol:
                print("Validation Error: For 'spot' category, 'symbol' is required.")
                return False

        else:
            print(f"Validation Error: Unknown category '{self.category}'.")
            return False

        # If all checks pass
        return True