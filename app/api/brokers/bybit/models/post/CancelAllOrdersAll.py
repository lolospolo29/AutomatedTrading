from dataclasses import dataclass, field
from typing import Optional, List

from app.api.brokers.ResponseParameters import ResponseParameters
from app.api.brokers.bybit.models.post.CancelledOrder import CancelledOrder


@dataclass
class CancelAllOrdersAll(ResponseParameters):
    list: Optional[List[CancelledOrder]] = field(default=List[CancelledOrder])
