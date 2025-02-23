from pydantic import BaseModel



class Result(BaseModel):
    result_id: str
    strategy:str

    equity_curve: list

    no_of_trades: int = 0
    winrate:float = 0.0
    risk_ratio:float = 0.0
    win_count:int = 0
    break_even_count:int = 0
    loss_count:int = 0
    pnl_percentage:float = 0.0
    average_win:float = 0.0
    average_loss:float = 0.0
    average_duration:float = 0.0
    highest_profit:float = 0.0
    max_drawdown:float = 0.0