from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.models.get.TickerOption import TickerOption


@dataclass
class TickersOption(ResponseParams):

    category: Optional[str] = field(default=None)
    list: Optional[List[TickerOption]] = field(default=List[TickerOption])
