from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BrokerFunding:
    category: Optional[str] = field(default=None)
    fundingRate: Optional[str] = field(default=None)
    fundingRateTimestamp: Optional[str] = field(default=None)
