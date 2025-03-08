from dataclasses import dataclass, field
from typing import Optional

from files.api.GETParams import GETParams


@dataclass
class OrderHistory(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None) # not in order
    orderId: Optional[str] = field(default=None) # not in order
    orderLinkId: Optional[str] = field(default=None) # not in order
    orderFilter: Optional[str] = field(default=None) # not in order
    orderStatus: Optional[str] = field(default=None) # not in order
    startTime: Optional[int] = field(default=None) # not in order
    endTime: Optional[int] = field(default=None) # not in order
    settleCoin: Optional[str] = field(default=None) # not in order
    limit: Optional[int] = field(default=None) # not in order max 200
    cursor: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            return True
        return False
