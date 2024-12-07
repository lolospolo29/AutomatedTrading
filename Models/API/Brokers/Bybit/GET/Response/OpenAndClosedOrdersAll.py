from dataclasses import dataclass, field
from typing import Optional, List

from Models.API.Brokers.Bybit.GET.Response.SubModels.Orders import Orders
from Models.API.ResponseParams import ResponseParams


@dataclass
class OpenAndClosedOrdersAll(ResponseParams):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Orders]] = field(default=List[Orders])
