from enum import Enum


class RateLimitEnum(Enum):
    return_open_and_closed_order = 10
    return_position_info = 10
    amend_order = 10
    return_order_history = 2
    cancel_all_orders = 10
    cancel_order = 10
    place_order  = 10
    set_leverage = 10
