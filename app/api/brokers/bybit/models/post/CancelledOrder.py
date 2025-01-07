from dataclasses import dataclass, field
from typing import Optional

from app.api.ResponseMapper import ResponseMapper


@dataclass
class CancelledOrder(ResponseMapper):
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
