from dataclasses import dataclass, field
from typing import Optional

from Models.API.GETParams import GETParams


@dataclass
class Tickers(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    expDate: Optional[str] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if not self.category:
            raise ValueError("The 'category' parameter is required.")
