from pydantic import BaseModel

class ProfitStopEntry(BaseModel):
    profit: float=None
    stop: float=None
    entry: float=None
    percentage: float = 0.0  # Default value for percentage
