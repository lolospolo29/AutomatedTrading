from pydantic import BaseModel


class BrokerRisk(BaseModel):
    name: str
    leverage_per_asset:dict[str, float]
    wallet_balance:float
    max_drawdown:float
    current_pnl:float