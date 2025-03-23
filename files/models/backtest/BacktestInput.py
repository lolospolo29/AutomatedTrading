from typing import Optional

from pydantic import BaseModel, Field


class BacktestInput(BaseModel):
    strategy: str
    test_assets: Optional[list[str]] = Field(alias="testAssets", default=[])
    trade_limit:int = Field(alias="tradeLimit",default=2)
