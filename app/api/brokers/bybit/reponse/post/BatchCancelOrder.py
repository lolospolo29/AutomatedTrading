from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.models.post.BatchCanceledOrder import BatchCanceledOrder


@dataclass
class BatchCancelOrder(ResponseParams):

    category: Optional[List[BatchCanceledOrder]] = field(default=List[BatchCanceledOrder])
