from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseMapper import ResponseMapper
from app.api.brokers.bybit.models.get.Positions import Positions


@dataclass
class PositionInfoAll(ResponseMapper):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Positions]] = field(default=List[Positions])

