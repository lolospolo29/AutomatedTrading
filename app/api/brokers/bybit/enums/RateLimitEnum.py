from enum import Enum


class RateLimitEnum(Enum):
    returnOpenAndClosedOrder = 10
    returnPositionInfo = 10
    returnTickers = 10
    returnTickersLinearInverse = 10
    returnTickersOption = 10
    returnTickersSpot = 10
    addOrReduceMargin = 50
    amendOrder = 10
    cancelAllOrders = 10
    cancelOrder = 10
    placeOrder = 10
    setLeverage = 10
