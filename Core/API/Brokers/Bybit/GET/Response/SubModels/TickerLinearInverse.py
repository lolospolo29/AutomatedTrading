from dataclasses import dataclass, field
from typing import Optional

from Core.API.ResponseParams import ResponseParams


@dataclass
class TickerLinearInverse(ResponseParams):

    symbol: Optional[str] = field(default=None)
    lastPrice: Optional[str] = field(default=None)
    indexPrice: Optional[str] = field(default=None)
    markPrice: Optional[str] = field(default=None)
    prevPrice24h: Optional[str] = field(default=None)
    price24hPcnt: Optional[str] = field(default=None)
    highPrice24h: Optional[str] = field(default=None)
    lowPrice24h: Optional[str] = field(default=None)
    prevPrice1h: Optional[str] = field(default=None)
    openInterest: Optional[str] = field(default=None)
    openInterestValue: Optional[str] = field(default=None)
    turnover24h: Optional[str] = field(default=None)
    volume24h: Optional[str] = field(default=None)
    fundingRate: Optional[str] = field(default=None)
    nextFundingTime: Optional[str] = field(default=None)
    predictedDeliveryPrice: Optional[str] = field(default=None)
    basisRate: Optional[str] = field(default=None)
    basis: Optional[str] = field(default=None)
    deliveryFeeRate: Optional[str] = field(default=None)
    deliveryTime: Optional[str] = field(default=None)
    ask1Size: Optional[str] = field(default=None)
    bid1Price: Optional[str] = field(default=None)
    ask1Price: Optional[str] = field(default=None)
    bid1Size: Optional[str] = field(default=None)