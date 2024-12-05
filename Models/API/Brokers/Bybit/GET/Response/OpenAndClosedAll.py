from dataclasses import dataclass, field
from typing import Optional

from Models.API.ResponseParams import ResponseParams


@dataclass
class OpenAndClosedAll(ResponseParams):

    category: Optional[str] = field(default=None)
    nextPageCursor: Optional[str] = field(default=None)
    lastPrice: Optional[str] = field(default=None)
    orderId: Optional[str] = field(default=None)
    orderLinkId: Optional[str] = field(default=None)
    blockTradeId: Optional[str] = field(default=None)
    symbol: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)
    qty: Optional[str] = field(default=None)
    side: Optional[str] = field(default=None)
    isLeverage: Optional[str] = field(default=None)
    positionIdx: Optional[int] = field(default=None)
    orderStatus: Optional[str] = field(default=None)
    createType: Optional[str] = field(default=None)
    cancelType: Optional[str] = field(default=None)
    rejectReason: Optional[str] = field(default=None)
    avgPrice: Optional[str] = field(default=None)
    leavesQty: Optional[str] = field(default=None)
    leavesValue: Optional[str] = field(default=None)
    cumExecQty: Optional[str] = field(default=None)
    cumExecValue: Optional[str] = field(default=None)
    cumExecFee: Optional[str] = field(default=None)
    timeInForce: Optional[str] = field(default=None)
    orderType: Optional[str] = field(default=None)
    stopOrderType: Optional[str] = field(default=None)
    orderlv: Optional[str] = field(default=None)
    marketUnit: Optional[str] = field(default=None)
    triggerPrice: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
    ocoTriggerBy: Optional[str] = field(default=None)
    tpLimitPrice: Optional[str] = field(default=None)
    slLimitPrice: Optional[str] = field(default=None)
    tpTriggerBy: Optional[str] = field(default=None)
    slTriggerBy: Optional[str] = field(default=None)
    triggerDirection: Optional[int] = field(default=None)
    triggerBy: Optional[str] = field(default=None)
    lastPriceOnCreated: Optional[str] = field(default=None)
    reduceOnly: Optional[bool] = field(default=None)
    closeOnTrigger: Optional[bool] = field(default=None)
    placeType: Optional[str] = field(default=None)
    smpType: Optional[str] = field(default=None)
    smpGroup: Optional[int] = field(default=None)
    smpOrderId: Optional[str] = field(default=None)
    createdTime: Optional[str] = field(default=None)
    updatedTime: Optional[str] = field(default=None)

    def jsonMapToClass(self):
        pass