from enum import Enum


class MongoEndPointEnum(Enum):
    OPENTRADES = 'OpenTrades'
    CLOSEDTRADES = 'ClosedTrades'
    OPENORDERS = 'OpenOrders'
    CLOSEDORDERS = 'ClosedOrders'