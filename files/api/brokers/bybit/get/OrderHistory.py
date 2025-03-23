from typing import Optional

from pydantic import BaseModel, Field


class OrderHistory(BaseModel):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = Field(default=None)
    baseCoin: Optional[str] = Field(default=None) # not in order
    orderId: Optional[str] = Field(default=None) # not in order
    orderLinkId: Optional[str] = Field(default=None) # not in order
    orderFilter: Optional[str] = Field(default=None) # not in order
    orderStatus: Optional[str] = Field(default=None) # not in order
    startTime: Optional[int] = Field(default=None) # not in order
    endTime: Optional[int] = Field(default=None) # not in order
    settleCoin: Optional[str] = Field(default=None) # not in order
    limit: Optional[int] = Field(default=None) # not in order max 200
    cursor: Optional[str] = Field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            return True
        return False
