from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.models.post.BatchAmendedOrder import BatchAmendedOrder


@dataclass
class BatchAmendOrder(ResponseParams):

    category: Optional[List[BatchAmendedOrder]] = field(default=List[BatchAmendedOrder])
