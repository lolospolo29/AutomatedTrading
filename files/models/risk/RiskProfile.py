import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from files.models.PyObjectId import PyObjectId
from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from files.models.risk.Fundamentals import Fundamentals
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent



class RiskProfile(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    risk_profile_id: str = Field(alias="riskProfileId",  default_factory=lambda: uuid.uuid4().__str__())
    status: str = Field(default="")
    current_quarter: str = Field(alias="currentQuarter", default="")
    weekly_hedging: str = Field(alias="weeklyHedging", default="")
    daily_hedging: str = Field(alias="dailyHedging", default="")
    daily_profile: str = Field(alias="dailyProfile", default="")  # todo: profiler with weekday / protraction
    weekly_profile: str = Field(alias="weeklyProfile", default="")
    current_htf_pd: Optional[list[PDArray]] = Field(alias="currentHTF", default=None, exclude=True)
    stdv_frameworks: Optional[list[FrameWork]] = Field(alias="stdvFrameworks", default=None, exclude=True)
    smt_detected: Optional[dict[int, Structure]] = Field(alias="smtDetected", default=None, exclude=True)
    atr: float = Field(alias="atr", default=0)
    potential_no_trade_conditions: Optional[list[str]] = Field(alias="potentialNoTradeConditions", default=None, exclude=True)
    news: Optional[list[NewsEvent]] = Field(alias="newsEvents", default=None, exclude=True)
    fundamentals: Optional[Fundamentals] = Field(alias="fundamentals", default=None, exclude=True)

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated

