from dataclasses import dataclass, field
from typing import Optional

from Models.API.GETParams import GETParams


# GET /v5/position/list
# Query real-time position data,
# such as position size, cumulative realizedPNL.
@dataclass
class PositionInfo(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    limit: Optional[str] = field(default=None)
    cursor: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if not self.category:
            raise ValueError("The 'category' parameter is required.")
