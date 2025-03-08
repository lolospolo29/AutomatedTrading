from typing import Optional

from pydantic import BaseModel

from files.models.asset.Relation import Relation  # Ensure correct import
from files.models.trade.Order import Order  # Ensure correct import


class Trade(BaseModel):
    orders: Optional[list[Order]] = None  #
    relation: Optional[Relation] = None
    tradeId: Optional[str] = None
    category: Optional[str] = None
    side: Optional[str] = None
    tpslMode: Optional[str] = None
    unrealisedPnl: Optional[str] = None
    leverage: Optional[str] = None
    size: Optional[str] = None
    tradeMode: Optional[int] = None
    updatedTime: Optional[str] = None
    createdTime: Optional[str] = None
