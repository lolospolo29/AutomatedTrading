import uuid
from typing import Optional

from pydantic import Field, BaseModel

from files.models.PyObjectId import PyObjectId
from files.models.asset.Candle import Candle
from files.models.trade.Order import Order


class TradeResult(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    trade_result_id:str = Field(alias="tradeResultId",default_factory=lambda: uuid.uuid4().__str__())
    trade_id: str = Field(alias="tradeId")
    is_closed:bool = Field(alias="isClosed",default=False)
    is_win:bool = Field(alias="isWin",default=False)
    deleted_orders:Optional[list[Order]] = Field(alias="deletedOrders",default=[],exclude=True)
    filled_orders:Optional[list[Order]] = Field(alias="filledOrders",default=[],exclude=True)
    active_orders:Optional[list[Order]] = Field(alias="activeOrders",default=[],exclude=True)
    pending_orders:Optional[list[Order]] = Field(alias="pendingOrders",default=[],exclude=True)
    last_candle:Candle = Field(alias="lastCandle",default=None,exclude=True)
    side:str = Field(default="")
    qty:float = Field(default=0)
    highest_price:float = Field(alias="highestPrice",default=float("-inf"))
    lowest_price:float = Field(alias="lowestPrice",default=float("inf"))

    # after process
    pnl_percentage:float = Field(alias="pnlPercentage",default=float("-inf"))
    entry_time:str =  Field(alias="entryTime",default="")
    exit_time:str = Field(alias="exitTime",default="")
    max_drawdown:float = Field(alias="maxDrawdown",default=0)
    entry_price:float = Field(alias="entryPrice",default=0)
    stop:float = Field(default=0)
    take_profit:float = Field(alias="takeProfit",default=0)
    risk_reward_ratio: float = Field(alias="riskRewardRatio",default=0)

    class Config:
        json_encoders = {PyObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated