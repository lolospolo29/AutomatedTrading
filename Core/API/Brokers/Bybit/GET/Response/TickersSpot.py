from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.GET.Response.SubModels.TickerSpot import TickerSpot
from Core.API.ResponseParams import ResponseParams


@dataclass
class TickersSpot(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerSpot]] = field(default=List[TickerSpot])
