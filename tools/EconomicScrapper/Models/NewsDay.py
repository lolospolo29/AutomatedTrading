import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent

class NewsDay(BaseModel):

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    news_day_id:int = Field(alias="newsDayId", default_factory=uuid.uuid4)
    day_iso: datetime = Field(alias="dayIso")
    news_events : Optional[list[NewsEvent]] = Field(default=None,exclude=True)