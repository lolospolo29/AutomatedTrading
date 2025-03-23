from typing import Optional

from pydantic import BaseModel, Field


# get /v5/position/list
# Query real-time position data,
# such as position size, cumulative realizedPNL.
# symbol parameter is supported to be passed with multiple symbols
# up to 10, e.g., "symbol=BTCUSD,ETHUSD"
class PositionInfo(BaseModel):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = Field(default=None)
    baseCoin: Optional[str] = Field(default=None) # not in order
    settleCoin: Optional[str] = Field(default=None) # not in order
    limit: Optional[int] = Field(default=None) # not in order max 200
    cursor: Optional[str] = Field(default=None)

    def validate(self) -> bool:
        """Validate required parameters."""
        if self.category:
            if self._validateLinear() and self._validateBaseCoin():
                return True
        return False

    def _validateBaseCoin(self) -> bool:
        """Validate base coin parameters."""
        if self.baseCoin:
            if self.category == "option":
                return True
            return False
        return True

    def _validateLinear(self):
        if self.category == "linear":
            if self.settleCoin or self.symbol:
                return True
            return False
        return True