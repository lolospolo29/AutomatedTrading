from dataclasses import dataclass, field
from typing import Optional

from Models.API.ResponseParams import ResponseParams


@dataclass
class TickerOption(ResponseParams):

    symbol: Optional[str] = field(default=None)
    bid1Price: Optional[str] = field(default=None)
    bid1Size: Optional[str] = field(default=None)
    bid1lv: Optional[str] = field(default=None)
    ask1Price: Optional[str] = field(default=None)
    ask1Size: Optional[str] = field(default=None)
    ask1lv: Optional[str] = field(default=None)
    lastPrice: Optional[str] = field(default=None)
    highPrice24h: Optional[str] = field(default=None)
    lowPrice24h: Optional[str] = field(default=None)
    markPrice: Optional[str] = field(default=None)
    indexPrice: Optional[str] = field(default=None)
    marklv: Optional[str] = field(default=None)
    underlyingPrice: Optional[str] = field(default=None)
    openInterest: Optional[str] = field(default=None)
    turnover24h: Optional[str] = field(default=None)
    volume24h: Optional[str] = field(default=None)
    totalVolume: Optional[str] = field(default=None)
    totalTurnover: Optional[str] = field(default=None)
    delta: Optional[str] = field(default=None)
    gamma: Optional[str] = field(default=None)
    vega: Optional[str] = field(default=None)
    theta: Optional[str] = field(default=None)
    predictedDeliveryPrice: Optional[str] = field(default=None)
    change24h: Optional[str] = field(default=None)