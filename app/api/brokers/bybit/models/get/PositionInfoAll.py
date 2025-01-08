from dataclasses import dataclass, field
from typing import Optional, List

from app.api.brokers.ResponseParameters import ResponseParameters
from app.api.brokers.bybit.models.get.Positions import Positions


@dataclass
class PositionInfoAll(ResponseParameters):

    list: Optional[List[Positions]] = field(default=List[Positions])

