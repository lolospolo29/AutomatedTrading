from typing import Optional

from pydantic import BaseModel


class Relation(BaseModel):
    asset: str
    broker: str
    strategy: str
    max_trades: int
    id: Optional[int]

    model_config = {
        "frozen": True
    }

    def __str__(self):
        return f"{self.asset} {self.broker} {self.strategy}"
