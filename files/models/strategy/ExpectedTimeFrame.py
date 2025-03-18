from pydantic import BaseModel


class ExpectedTimeFrame(BaseModel):
    timeframe: int
    max_len: int
