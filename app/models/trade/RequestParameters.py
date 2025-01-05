from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RequestParameters:
    baseCoin: Optional[str] = field(default=None)
    settleCoin: Optional[str] = field(default=None)
    openOnly: Optional[str] = field(default=None)
    limit: Optional[int] = field(default=None)
    cursor: Optional[str] = field(default=None)
    category: Optional[str] = field(default=None)
    orderFilter: Optional[str] = field(default=None)
    stopOrderType: Optional[bool] = field(default=None)
    symbol: Optional[str] = field(default=None)
    sellLeverage: Optional[str] = field(default=None)
    buyLeverage: Optional[str] = field(default=None)
    margin: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
