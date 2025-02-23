from pydantic import BaseModel

from app.models.trade.Order import Order


class TradeResult(BaseModel):
    # while process
    tradeId: str
    is_closed:bool = False
    deleted_orders:list[Order] # deleted
    filled_orders:list[Order] # filled
    active_orders:list[Order] # placed but not filled
    pending_orders:list[Order] # not activated
    side:str = ""
    qty:float = 0.0

    # after process
    pnl_percentage:float = 0.0 # aftermath
    entry_time:str = ""
    exit_time:str = ""
    max_drawdown:float = 0.0
    entry_price:float = 0.0
    stop:float = 0.0
    take_profit:float = 0.0