from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.GET.Response.SubModels.TickerLinearInverse import TickerLinearInverse
from Core.API.ResponseParams import ResponseParams


@dataclass
class TickersLinearInverse(ResponseParams):
    category: Optional[str] = field(default=None)
    list: Optional[List[TickerLinearInverse]] = field(default=List[TickerLinearInverse])