from dataclasses import dataclass, field
from typing import Optional

from Core.API.ResponseParams import ResponseParams


@dataclass
class BatchPlacedOrder(ResponseParams):

    category: Optional[str] = field(default=None)
    symbol: Optional[str] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    createAt: Optional[str] = field(default=None)
    code: Optional[str] = field(default=None)
    msg: Optional[str] = field(default=None)

