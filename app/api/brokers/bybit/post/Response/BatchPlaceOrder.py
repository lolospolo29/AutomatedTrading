from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.post.Response.SubModels.BatchPlacedOrder import BatchPlacedOrder


@dataclass
class BatchPlaceOrder(ResponseParams):

    category: Optional[List[BatchPlacedOrder]] = field(default=List[BatchPlacedOrder])

