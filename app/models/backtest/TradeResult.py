from pydantic import BaseModel


class TradeResult(BaseModel):
    tradeId: str

    is_closed:bool = False
    is_active:bool = False
    side:str = ""
    pnl_percentage:float = 0.0
    qty:float = 0.0
    entry_time:str = ""
    exit_time:str = ""
    max_drawdown:float = 0.0
    entry_price:float = 0.0
    stop:float = 0.0
    take_profit:float = 0.0