from pydantic import BaseModel


class BacktestInput(BaseModel):
    strategy: str
    test_assets: list[str]
    trade_limit:int=2