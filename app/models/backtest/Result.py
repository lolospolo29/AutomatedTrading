from pydantic import BaseModel



class Result(BaseModel):
    result_id: str = ""
    no_of_trades: int
    winrate:float
    break_even_count:int
    win_count:int
    loss_count:int
    pnl:float
    pnl_percentage:float
    risk_ratio:float
    qty:float
    average_win:float
    average_loss:float
    average_pips:float
    average_duration:float
    average_entry_time:float
    highest_profit:float
    max_drawdown:float
