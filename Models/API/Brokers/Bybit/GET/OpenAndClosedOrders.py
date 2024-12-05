from dataclasses import dataclass, field
from typing import Optional

from Models.API.GETParams import GETParams


@dataclass
class OpenAndClosedOrders(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    openOnly: Optional[str] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    limit: Optional[str] = field(default=None)
    cursor: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if not self.category:
            raise ValueError("The 'category' parameter is required.")
