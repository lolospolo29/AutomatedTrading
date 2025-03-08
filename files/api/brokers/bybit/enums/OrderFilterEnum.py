from enum import Enum


class OrderFilterEnum(Enum):
    ORDER = 'Order'
    TPSLORDER = 'tpslOrder'
    STOPORDER = 'StopOrder'
    OCOORDER = 'OcOOrder'
    BIDIRECTIONALTPSLORDER = 'BidDirectionalTpslOrder'



