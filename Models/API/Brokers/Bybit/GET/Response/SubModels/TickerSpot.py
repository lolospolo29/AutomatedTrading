from dataclasses import dataclass, field
from typing import Optional

from Models.API.ResponseParams import ResponseParams


@dataclass
class TickerSpot(ResponseParams):

    symbol: Optional[str] = field(default=None)
    bid1Price: Optional[str] = field(default=None)
    bid1Size: Optional[str] = field(default=None)
    ask1Size: Optional[str] = field(default=None)
    ask1Price: Optional[str] = field(default=None)
    lastPrice: Optional[str] = field(default=None)
    prevPrice24h: Optional[str] = field(default=None)
    price24hPcnt: Optional[str] = field(default=None)
    highPrice24h: Optional[str] = field(default=None)
    lowPrice24h: Optional[str] = field(default=None)
    turnover24h: Optional[str] = field(default=None)
    volume24h: Optional[str] = field(default=None)
    usdIndexPrice: Optional[str] = field(default=None)