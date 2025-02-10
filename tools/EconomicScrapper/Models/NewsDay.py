from typing import Optional

from pydantic import BaseModel

from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class NewsDay(BaseModel):
    """
    Represents a specific day with associated news events.

    This class is used to encapsulate date-specific information and a collection
    of associated news events. It serves as the main structure for handling news
    data categorized by individual dates. Typically used in contexts where
    chronological organization of events is required.

    """
    day_iso: str
    news_events : Optional[list[NewsEvent]] = None
