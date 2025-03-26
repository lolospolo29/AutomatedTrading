from typing import Optional

from pydantic import BaseModel, Field

from files.models.strategy.StrategyDTO import StrategyDTO


class BacktestInput(BaseModel):
    strategy: StrategyDTO = Field(alias="strategy",default=None)
    test_assets: Optional[list[str]] = Field(alias="testAssets", default=[])
    trade_limit:int = Field(alias="tradeLimit",default=2)
