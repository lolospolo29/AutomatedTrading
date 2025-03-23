import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from files.models.PyObjectId import PyObjectId


class Result(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    name: str= Field(default=None)
    asset_class_id: Optional[int] = Field(default=None,alias="assetClassId")

    result_id: str = Field(alias="resultId", default_factory=lambda: uuid.uuid4().__str__())
    strategy:str
    asset:str

    no_of_trades: Optional[int] = Field(default=None, alias="noOfTrades")
    winrate:Optional[float] = None
    risk_ratio:Optional[float] = Field(default=None, alias="riskRatio")
    win_count: Optional[int] = Field(default=None, alias="winCount")
    break_even_count: Optional[int] = Field(default=None, alias="breakEvenCount")
    loss_count: Optional[int] = Field(default=None, alias="lossCount")
    pnl_percentage:Optional[float] = Field(default=None, alias="pnlPercentage")
    average_win:Optional[float] = Field(default=None, alias="averageWin")
    average_loss:Optional[float] = Field(default=None, alias="averageLoss")
    average_duration:Optional[float] = Field(default=None, alias="averageDuration")
    max_drawdown:Optional[float] = Field(default=None, alias="maxDrawdown")

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated