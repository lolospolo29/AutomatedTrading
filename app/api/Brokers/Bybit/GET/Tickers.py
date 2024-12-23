from dataclasses import dataclass, field
from typing import Optional

from app.API.GETParams import GETParams


# GET /v5/market/tickers
# Query for the latest price snapshot, best bid/ask price,
# and trading volume in the last 24 hours.
# Covers: Spot / USDT perpetual / USDC contract / Inverse contract / Option
@dataclass
class Tickers(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    baseCoin: Optional[str] = field(default=None)
    expDate: Optional[str] = field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            return self.validateOption()
        return False

    def validateOption(self) -> bool:
        """Validate option parameters."""
        if self.category == "option":
            if self.symbol or self.baseCoin:
                return True
            return False
        return True
