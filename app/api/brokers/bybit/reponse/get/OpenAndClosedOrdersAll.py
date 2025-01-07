from dataclasses import dataclass, field
from typing import Optional, List

from app.api.brokers.bybit.models.get.Orders import Orders
from app.api.ResponseMapper import ResponseMapper


@dataclass
class OpenAndClosedOrdersAll(ResponseMapper):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Orders]] = field(default=List[Orders])
