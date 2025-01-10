from enum import Enum


class EndPointEnum(Enum):
    OPENANDCLOSED = "/v5/order/realtime"
    POSITIONINFO = "/v5/position/list"
    TICKERS = "/v5/market/tickers"
    MARGIN = "/v5/position/add-margin"
    AMEND = "/v5/order/amend"
    CANCELALL = "/v5/order/cancel-all"
    CANCEL = "/v5/order/cancel"
    PLACEORDER = "/v5/order/create"
    SETLEVERAGE = "/v5/order/set-leverage"
    SETTRADINGSTOP = "/v5/position/trading-stop"
    BATCHPLACE = "/v5/order/create-batch"
    AMENDBATCH = "/v5/order/amend-batch"
    CANCELBATCH = "/v5/order/cancel-batch"
    INSTRUMENT = "/v5/market/instruments-info"
    HISTORY = "/v5/order/history"