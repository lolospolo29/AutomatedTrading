from enum import Enum


class RateLimitEnum(Enum):
    returnOpenAndClosedOrder = 10
    returnPositionInfo = 10
    amendOrder = 10
    returnOrderHistory = 2
    cancelAllOrders = 10
    cancelOrder = 10
    placeOrder = 10
    setLeverage = 10
