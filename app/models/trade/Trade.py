from pydantic import BaseModel
from typing import Optional, List
from app.models.trade.Order import Order  # Ensure correct import
from app.models.asset.Relation import Relation  # Ensure correct import

class Trade(BaseModel):
    orders: Optional[list[Order]] = None  #
    relation: Optional[Relation] = None
    id: Optional[str] = None
    category: Optional[str] = None
    side: Optional[str] = None
    tpslMode: Optional[str] = None
    unrealisedPnl: Optional[str] = None
    leverage: Optional[str] = None
    size: Optional[str] = None
    tradeMode: Optional[int] = None
    updatedTime: Optional[str] = None
    createdTime: Optional[str] = None
