import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent

class NewsDay(BaseModel):

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    news_day_id:int
    day_iso: datetime
    news_events : Optional[list[NewsEvent]] = Field(exclude=True, default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if self.framework_id is None:
            self.framework_id = str(uuid.uuid4())
