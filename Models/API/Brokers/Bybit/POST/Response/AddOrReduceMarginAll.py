from dataclasses import dataclass, field
from typing import Optional

from Models.API.ResponseParams import ResponseParams


@dataclass
class AddOrReduceMarginAll(ResponseParams):

    symbol: Optional[str] = field(default=None)
    positionIdx: Optional[str] = field(default=None)
    riskId: Optional[int] = field(default=None)
    riskLimitValue: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    avgPrice: Optional[str] = field(default=None)
    liqPrice: Optional[str] = field(default=None)
    bustPrice: Optional[str] = field(default=None)
    markPrice: Optional[str] = field(default=None)
    positionValue: Optional[str] = field(default=None)
    leverage: Optional[str] = field(default=None)
    autoAddMargin: Optional[int] = field(default=None)
    positionStatus: Optional[str] = field(default=None)
    positionIM: Optional[str] = field(default=None)
    positionMM: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    trailingStop: Optional[str] = field(default=None)
    unrealisedPnl: Optional[str] = field(default=None)
    cumRealisedPnl: Optional[str] = field(default=None)
    createdTime: Optional[str] = field(default=None)
    updatedTime: Optional[str] = field(default=None)

    def jsonMapToClass(self):
        pass