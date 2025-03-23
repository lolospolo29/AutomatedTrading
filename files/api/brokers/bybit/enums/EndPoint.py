from enum import Enum


class EndPointEnum(Enum):
    OPENANDCLOSED = "/v5/order/realtime"
    POSITIONINFO = "/v5/position/list"
    MARGIN = "/v5/position/add-margin"
    AMEND = "/v5/order/amend"
    CANCELALL = "/v5/order/cancel-all"
    CANCEL = "/v5/order/cancel"
    PLACEORDER = "/v5/order/create"
    SETLEVERAGE = "/v5/position/set-leverage"
    INSTRUMENT = "/v5/market/instruments-info"
    HISTORY = "/v5/order/history"
    FUNDING = "/v5/market/funding/history"