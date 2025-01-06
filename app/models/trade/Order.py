from datetime import datetime

from app.models.frameworks.FrameWork import FrameWork


class Order:
    # Self Defined Parameters
    tradeId: str
    status: str

    # to-do add risk type for ai training later

    entryFrameWork: FrameWork
    confirmations: list[FrameWork]

    createdAt: datetime
    openedAt: datetime
    closedAt: datetime
    updatedAt: datetime

    riskPercentage: float
    moneyAtRisk: float
    unrealisedPnL: float

    # Required on Broker
    orderLinkId: str
    orderType:str
    symbol: str
    category: str
    side: str
    qty: str #must be defined in Risk Manager

    # Must be set after sending Request
    orderId: str

    # Spot Logic
    isLeverage: int
    marketUnit: str
    orderFilter: str
    orderlv: str

    # Specific attributes (optional)
    stopLoss: str
    takeProfit: str
    price: str
    timeInForce: str
    closeOnTrigger: bool
    reduceOnly: bool

    # Conditional
    triggerPrice: str
    triggerBy:str
    tpTriggerBy: str
    slTriggerBy: str
    triggerDirection: int

    # Limit Logic attributes (optional)
    tpslMode: str
    tpLimitPrice: str
    tpOrderType: str
    slOrderType: str
    slLimitPrice: str

    def __init__(self):
        self.createdAt = datetime.now()

    def __setattr__(self, key, value):
        # Update updatedAt whenever an attribute is changed
        super().__setattr__(key, value)
        if key != 'updatedAt':  # Avoid recursive updates
            super().__setattr__('updatedAt', datetime.now())

    def toDict(self):
        def transform_value(key, value):
            """Applies necessary transformations to specific fields."""
            if isinstance(value, list):
                return [item.toDict() for item in value if hasattr(item, "toDict")]
            elif isinstance(value, datetime):
                return value.isoformat()
            elif hasattr(value, "toDict"):
                return value.toDict()
            return value

        return {
            "Order": {
                key: transform_value(key, getattr(self, key))
                if hasattr(self, key) else None
                for key in self.__annotations__.keys()
            }
        }
