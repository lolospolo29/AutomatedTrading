from dataclasses import dataclass, field
from typing import Optional

from files.api.GETParams import GETParams


# get /v5/market/funding/history
#Query for historical funding rates.
# Each symbol has a different funding interval. For example, if the interval is 8 hours and the current time is UTC 12,
# then it returns the last funding rate, which settled at UTC 8.
@dataclass
class FundingHistory(GETParams):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = field(default=None)
    startTime: Optional[str] = field(default=None) # exits but different enums
    endTime: Optional[str] = field(default=None) # exits but different enums
    limit: Optional[int] = field(default=None) # page size receiving

    def validate(self) -> bool:
        """Validate required parameters based on category and other conditions."""
        # Check if category is provided
        if not self.category:
            print("Validation Error: 'category' is required.")
            return False

        # If all checks pass
        return True


