from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.POST.Response.SubModels.BatchCanceledOrder import BatchCanceledOrder
from Core.API.ResponseParams import ResponseParams


@dataclass
class BatchCancelOrder(ResponseParams):

    category: Optional[List[BatchCanceledOrder]] = field(default=List[BatchCanceledOrder])
