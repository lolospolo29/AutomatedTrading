from typing import Optional

from pydantic import BaseModel

from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Trade import Trade


class StrategyResult(BaseModel):
    trade: Optional[Trade]=None
    status: Optional[str]=StrategyResultStatusEnum.NOCHANGE.value
