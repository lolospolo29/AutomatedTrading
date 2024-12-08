from dataclasses import dataclass, field
from typing import Optional, List

from Models.API.Brokers.Bybit.GET.Response.SubModels.TickerOption import TickerOption
from Models.API.ResponseParams import ResponseParams


@dataclass
class TickersOption(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerOption]] = field(default=List[TickerOption])
