from dataclasses import dataclass, field
from typing import Optional

from Models.API.POSTParams import POSTParams


@dataclass
class CancelOrder(POSTParams):
    # Required parameter
    category: str
    symbol: str

    # Either one Required
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)

    # Optional parameters
    orderFilter: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if not self.category and self.symbol and (self.orderId or self.orderLinkId):
            raise ValueError("The 'category' parameter is required.")
