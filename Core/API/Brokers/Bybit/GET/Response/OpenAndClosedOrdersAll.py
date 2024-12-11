from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.GET.Response.SubModels.Orders import Orders
from Core.API.ResponseParams import ResponseParams


@dataclass
class OpenAndClosedOrdersAll(ResponseParams):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Orders]] = field(default=List[Orders])
