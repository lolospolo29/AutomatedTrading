from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.get.Response.SubModels.TickerSpot import TickerSpot


@dataclass
class TickersSpot(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerSpot]] = field(default=List[TickerSpot])
