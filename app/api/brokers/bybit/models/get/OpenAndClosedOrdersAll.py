from dataclasses import dataclass, field
from typing import Optional, List

from app.api.brokers.ResponseParameters import ResponseParameters
from app.api.brokers.bybit.models.get.Orders import Orders


@dataclass
class OpenAndClosedOrdersAll(ResponseParameters):

    list: Optional[List[Orders]] = field(default=List[Orders])
