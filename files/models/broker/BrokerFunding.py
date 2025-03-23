from typing import Optional

from pydantic import Field, BaseModel


class BrokerFunding(BaseModel):
    category: Optional[str] = Field(default=None)
    symbol: Optional[str] = Field(default=None)
    fundingRate: Optional[str] = Field(default=None)
    fundingRateTimestamp: Optional[str] = Field(default=None)
