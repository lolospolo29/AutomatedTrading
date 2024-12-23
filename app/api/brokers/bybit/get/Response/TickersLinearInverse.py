from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.get.Response.SubModels.TickerLinearInverse import TickerLinearInverse


@dataclass
class TickersLinearInverse(ResponseParams):
    category: Optional[str] = field(default=None)
    list: Optional[List[TickerLinearInverse]] = field(default=List[TickerLinearInverse])