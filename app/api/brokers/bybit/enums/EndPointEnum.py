from enum import Enum


class EndPointEnum(Enum):
    OPENANDCLOSED = "/v5/order/realtime"
    POSITIONINFO = "/v5/position/list"