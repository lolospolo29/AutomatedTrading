from dataclasses import dataclass, field
from typing import Optional, List

from app.API.Brokers.Bybit.POST.Response.SubModels.BatchPlacedOrder import BatchPlacedOrder
from app.API.ResponseParams import ResponseParams


@dataclass
class BatchPlaceOrder(ResponseParams):

    category: Optional[List[BatchPlacedOrder]] = field(default=List[BatchPlacedOrder])

