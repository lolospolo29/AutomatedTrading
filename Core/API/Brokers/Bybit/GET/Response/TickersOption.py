from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.GET.Response.SubModels.TickerOption import TickerOption
from Core.API.ResponseParams import ResponseParams


@dataclass
class TickersOption(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerOption]] = field(default=List[TickerOption])
