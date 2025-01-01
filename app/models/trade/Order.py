from datetime import datetime

from app.models.frameworks.FrameWork import FrameWork
from app.models.frameworks.PDArray import PDArray


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
        return {
            "Order":{
                "tradeId": "" if not hasattr(self,"tradeId") else self.tradeId,
                "status": "" if not hasattr(self,"status") else self.status,
                "entryFrameWork": "" if not hasattr(self,"entryFrameWork") else self.entryFrameWork.toDict(),
                "confirmations": [framework.toDict() for framework in self.confirmations if not framework is None],
                "createdAt": "" if not hasattr(self,"createdAt") else self.createdAt.isoformat(),
                "openedAt": self.createdAt.isoformat() if not hasattr(self,"openedAt") else self.openedAt.isoformat(),
                "closedAt": self.createdAt.isoformat() if not hasattr(self,"closedAt") else self.closedAt.isoformat(),
                "updatedAt": self.createdAt.isoformat() if not hasattr(self,"updatedAt") else self.updatedAt.isoformat(),
                "riskPercentage": "" if not hasattr(self,"riskPercentage") else self.riskPercentage,
                "moneyAtRisk": "" if not hasattr(self,"moneyAtRisk") else self.moneyAtRisk,
                "unrealisedPnL": "" if not hasattr(self,"unrealisedPnL") else self.unrealisedPnL,
                "orderLinkId": "" if not hasattr(self,"orderLinkId") else self.orderLinkId,
                "orderType": "" if not hasattr(self,"orderType") else self.orderType,
                "symbol": "" if not hasattr(self,"symbol") else self.symbol,
                "category": "" if not hasattr(self,"category") else self.category,
                "side": "" if not hasattr(self,"side") else self.side,
                "qty": "" if not hasattr(self,"qty") else self.qty,
                "orderId": "" if not hasattr(self,"orderId") else self.orderId,
                "isLeverage": "" if not hasattr(self,"isLeverage") else self.isLeverage,
                "marketUnit": "" if not hasattr(self,"marketUnit") else self.marketUnit,
                "orderFilter": "" if not hasattr(self,"orderFilter") else self.orderFilter,
                "orderlv": "" if not hasattr(self,"orderlv") else self.orderlv,
                "stopLoss": "" if not hasattr(self,"stopLoss") else self.stopLoss,
                "takeProfit": "" if not hasattr(self,"takeProfit") else self.takeProfit,
                "price": "" if not hasattr(self,"price") else self.price,
                "timeInForce": "" if not hasattr(self,"timeInForce") else self.timeInForce,
                "closeOnTrigger": "" if not hasattr(self,"closeOnTrigger") else self.closeOnTrigger,
                "reduceOnly": "" if not hasattr(self,"reduceOnly") else self.reduceOnly,
                "triggerPrice": "" if not hasattr(self,"triggerPrice") else self.triggerPrice,
                "triggerBy": "" if not hasattr(self,"triggerBy") else self.triggerBy,
                "tpTriggerBy": "" if not hasattr(self,"tpTriggerBy") else self.tpTriggerBy,
                "slTriggerBy": "" if not hasattr(self,"slTriggerBy") else self.slTriggerBy,
                "tpslMode": "" if not hasattr(self,"tpslMode") else self.tpslMode,
                "tpLimitPrice": "" if not hasattr(self,"tpLimitPrice") else self.tpLimitPrice,
                "tpOrderType": "" if not hasattr(self,"tpOrderType") else self.tpOrderType,
                "slOrderType": "" if not hasattr(self,"slOrderType") else self.slOrderType,
                "slLimitPrice": "" if not hasattr(self,"slLimitPrice") else self.slLimitPrice,
            }
        }
frameWork = PDArray("name","BUY")

o = Order()
o.tradeId = "123"
o.status = "PENDING"
o.entryFrameWork = frameWork
o.confirmations = []
o.confirmations.append(frameWork)
print(o.toDict())