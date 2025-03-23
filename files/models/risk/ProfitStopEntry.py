from pydantic import BaseModel, Field


class ProfitStopEntry(BaseModel):
    profit: float = Field(default=0.0)
    stop: float= Field(default=0.0)
    entry: float= Field(default=0.0)
    percentage: float = Field(default=0.0)
