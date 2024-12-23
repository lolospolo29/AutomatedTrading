from dataclasses import dataclass, field
from typing import Optional

from app.API.ResponseParams import ResponseParams


@dataclass
class CancelOrderAll(ResponseParams):

    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
