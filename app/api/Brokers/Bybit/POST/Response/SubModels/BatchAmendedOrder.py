from dataclasses import dataclass, field
from typing import Optional

from app.API.ResponseParams import ResponseParams


@dataclass
class BatchAmendedOrder(ResponseParams):

    category: Optional[str] = field(default=None)
    symbol: Optional[str] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)

