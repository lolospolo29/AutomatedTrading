from typing import Optional

from pydantic import BaseModel, Field


class RequestParameters(BaseModel):
    brokerId:str
    positionIdx: Optional[int] = Field(default=None)
    baseCoin: Optional[str] = Field(default=None)
    settleCoin: Optional[str] = Field(default=None)
    openOnly: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=None)
    cursor: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    orderFilter: Optional[str] = Field(default=None)
    stopOrderType: Optional[bool] = Field(default=None)
    symbol: Optional[str] = Field(default=None)
    sellLeverage: Optional[str] = Field(default=None)
    buyLeverage: Optional[str] = Field(default=None)
    margin: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    orderId: Optional[str] = Field(default=None)
    orderLinkId: Optional[str] = Field(default=None)
    expDate: Optional[str] = Field(default=None)
    orderlv: Optional[str] = Field(default=None)
    triggerPrice: Optional[str] = Field(default=None)
    price: Optional[str] = Field(default=None)
    tpslMode: Optional[str] = Field(default=None)
    takeProfit: Optional[str] = Field(default=None)
    stopLoss: Optional[str] = Field(default=None)
    tpTriggerBy: Optional[str] = Field(default=None)
    slTriggerBy: Optional[str] = Field(default=None)
    triggerBy: Optional[str] = Field(default=None)
    tpLimitPrice: Optional[str] = Field(default=None)
    slLimitPrice: Optional[str] = Field(default=None)
    isLeverage: Optional[int] = Field(default=None)
    marketUnit: Optional[str] = Field(default=None)
    triggerDirection: Optional[int] = Field(default=None)
    timeInForce: Optional[str] = Field(default=None)
    reduceOnly: Optional[bool] = Field(default=None)
    closeOnTrigger: Optional[bool] = Field(default=None)
    smpType: Optional[str] = Field(default=None)
    mmp: Optional[bool] = Field(default=None)
    tpOrderType: Optional[str] = Field(default=None)
    slOrderType: Optional[str] = Field(default=None)
    orderType: Optional[str] = Field(default=None)
    side: Optional[str] = Field(default=None)
    qty: Optional[str] = Field(default=None)
    startTime: Optional[int] = Field(default=None)
    endTime: Optional[int] = Field(default=None)

    def __str__(self):
        # Filter out fields with None values
        non_none_fields = {key: value for key, value in self.__dict__.items() if value is not None}
        # Create a string representation
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in non_none_fields.items())})"