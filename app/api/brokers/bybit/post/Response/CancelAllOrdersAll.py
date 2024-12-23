from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.post.Response.SubModels.CancelledOrder import CancelledOrder


@dataclass
class CancelAllOrdersAll(ResponseParams):
    list: Optional[List[CancelledOrder]] = field(default=List[CancelledOrder])
    success: Optional[str] = field(default=None)
