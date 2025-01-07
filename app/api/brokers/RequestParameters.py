from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RequestParameters:

    positionIdx: Optional[int] = field(default=None)
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
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    expDate: Optional[str] = field(default=None)
    orderlv: Optional[str] = field(default=None)
    triggerPrice: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)
    triggerBy: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)
    isLeverage: Optional[int] = field(default=None)
    marketUnit: Optional[str] = field(default=None)
    triggerDirection: Optional[int] = field(default=None)
    timeInForce: Optional[str] = field(default=None)
    reduceOnly: Optional[bool] = field(default=None)
    closeOnTrigger: Optional[bool] = field(default=None)
    smpType: Optional[str] = field(default=None)
    mmp: Optional[bool] = field(default=None)
    tpOrderType: Optional[str] = field(default=None)
    slOrderType: Optional[str] = field(default=None)
    broker: Optional[str] = field(default=None)
    orderType: Optional[str] = field(default=None)
    side: Optional[str] = field(default=None)
    qty: Optional[str] = field(default=None)

    def __str__(self):
        # Filter out fields with None values
        non_none_fields = {key: value for key, value in self.__dict__.items() if value is not None}
        # Create a string representation
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in non_none_fields.items())})"




