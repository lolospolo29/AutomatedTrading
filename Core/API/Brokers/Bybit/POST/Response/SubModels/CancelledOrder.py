from dataclasses import dataclass, field
from typing import Optional

from Core.API.ResponseParams import ResponseParams


@dataclass
class CancelledOrder(ResponseParams):
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
