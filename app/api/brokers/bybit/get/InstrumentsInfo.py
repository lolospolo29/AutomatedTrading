from dataclasses import dataclass, field
from typing import Optional

from app.api.GETParams import GETParams


# get /v5/market/instruments-info
# Query for the instrument specification of online trading pairs.
@dataclass
class InstrumentsInfo(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None) # not in order
    settleCoin: Optional[str] = field(default=None) # not in order
    limit: Optional[int] = field(default=None) # not in order max 200
    cursor: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
                return True
        return False
