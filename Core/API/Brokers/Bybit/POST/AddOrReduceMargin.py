from dataclasses import dataclass, field
from typing import Optional

from Core.API.POSTParams import POSTParams


# POST /v5/position/add-margin
# Manually add or reduce margin for isolated margin position
@dataclass
class AddOrReduceMargin(POSTParams):
    # Required parameter
    category: str
    symbol: str
    margin: str

    # Optional parameters
    positionIdx: Optional[int] = field(default=None)

    def validate(self):
        """Validate required parameters."""
        if self.category and self.symbol and self.margin:
            return True
        return False
