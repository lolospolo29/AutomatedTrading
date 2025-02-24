from pydantic import BaseModel


class BacktestInput(BaseModel):
    strategy: str
    test_assets: list[str]