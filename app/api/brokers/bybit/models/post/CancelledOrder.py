from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CancelledOrder:
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
