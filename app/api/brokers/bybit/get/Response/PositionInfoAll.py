from dataclasses import dataclass, field
from typing import Optional, List

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.get.Response.SubModels.Positions import Positions


@dataclass
class PositionInfoAll(ResponseParams):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Positions]] = field(default=List[Positions])

