from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Order:
    # Required parameters
    status: bool
    riskPercentage: float
    moneyAtRisk: float
    leverage: float
    unrealisedPnL: float
    orderLinkId: str
    orderType:str

    symbol: str
    category: str
    side: str
    takeProfit: str
    stopLoss: str
    qty: str

    # Must be set after sending Request
    orderId: Optional[str] = field(default=None)

    # Specific attributes (optional)
    timeInForce: Optional[str] = field(default=None)
    closeOnTrigger: Optional[bool] = field(default=False)
    reduceOnly: Optional[bool] = field(default=False)
    tpOrderType: Optional[str] = field(default=None)
    slOrderType: Optional[str] = field(default=None)
    triggerDirection: Optional[int] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)

    # Limit Logic attributes (optional)
    tpslMode: Optional[str] = field(default=None)
    orderPrice: Optional[str] = field(default=None)
    triggerPrice: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)
