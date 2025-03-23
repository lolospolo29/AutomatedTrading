from typing import Optional

from pydantic import BaseModel, Field


# get /v5/market/funding/history
#Query for historical funding rates.
# Each symbol has a different funding interval. For example, if the interval is 8 hours and the current time is UTC 12,
# then it returns the last funding rate, which settled at UTC 8.
class FundingHistory(BaseModel):
    # Required parameter
    category: str

    # Optional parameters
    symbol: Optional[str] = Field(default=None)
    startTime: Optional[str] = Field(default=None) # exits but different enums
    endTime: Optional[str] = Field(default=None) # exits but different enums
    limit: Optional[int] = Field(default=None) # page size receiving

    def validate(self) -> bool:
        """Validate required parameters based on category and other conditions."""
        # Check if category is provided
        if not self.category:
            print("Validation Error: 'category' is required.")
            return False

        # If all checks pass
        return True