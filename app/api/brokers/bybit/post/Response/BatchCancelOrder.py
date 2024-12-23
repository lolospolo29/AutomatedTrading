from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.post.Response.SubModels.BatchCanceledOrder import BatchCanceledOrder


@dataclass
class BatchCancelOrder(ResponseParams):

    category: Optional[List[BatchCanceledOrder]] = field(default=List[BatchCanceledOrder])
