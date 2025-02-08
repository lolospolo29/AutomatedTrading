from pydantic import BaseModel


class ExpectedTimeFrame(BaseModel):
    timeframe: int
    max_Len: int
