from dataclasses import dataclass, field
from typing import Optional, List

from app.API.Brokers.Bybit.POST.Response.SubModels.BatchAmendedOrder import BatchAmendedOrder
from app.API.ResponseParams import ResponseParams


@dataclass
class BatchAmendOrder(ResponseParams):

    category: Optional[List[BatchAmendedOrder]] = field(default=List[BatchAmendedOrder])
