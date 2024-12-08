from dataclasses import dataclass, field
from typing import Optional, List

from Models.API.Brokers.Bybit.GET.Response.SubModels.TickerSpot import TickerSpot
from Models.API.ResponseParams import ResponseParams


@dataclass
class TickersSpot(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerSpot]] = field(default=List[TickerSpot])
