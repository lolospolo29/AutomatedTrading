from dataclasses import dataclass, field
from typing import Optional, List

from Core.API.Brokers.Bybit.GET.Response.SubModels.Positions import Positions
from Core.API.ResponseParams import ResponseParams


@dataclass
class PositionInfoAll(ResponseParams):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    list: Optional[List[Positions]] = field(default=List[Positions])

