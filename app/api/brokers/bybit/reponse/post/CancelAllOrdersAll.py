from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseMapper import ResponseMapper
from app.api.brokers.bybit.models.post.CancelledOrder import CancelledOrder


@dataclass
class CancelAllOrdersAll(ResponseMapper):
    list: Optional[List[CancelledOrder]] = field(default=List[CancelledOrder])
    success: Optional[str] = field(default=None)
