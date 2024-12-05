from dataclasses import dataclass, field
from typing import Optional

from Models.API.POSTParams import POSTParams


@dataclass
class CancelAllOrders(POSTParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    stopOrderType: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if not self.category:
            raise ValueError("The 'category' parameter is required.")
