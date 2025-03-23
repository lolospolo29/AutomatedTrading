from typing import Optional

from pydantic import BaseModel, Field

from files.models.trade.Trade import Trade


class StrategyResult(BaseModel):
    trade: Optional[Trade]=Field(default=None)
    status: Optional[str]= Field(default=None)