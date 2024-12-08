from dataclasses import dataclass, field
from typing import Optional

from Models.API.ResponseParams import ResponseParams


@dataclass
class AmendOrderAll(ResponseParams):

    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
