from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.POST.Response.SubModels.CancelledOrder import CancelledOrder
from Core.API.ResponseParams import ResponseParams


@dataclass
class CancelAllOrdersAll(ResponseParams):
    list: Optional[List[CancelledOrder]] = field(default=List[CancelledOrder])
    success: Optional[str] = field(default=None)
