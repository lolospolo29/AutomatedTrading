from dataclasses import dataclass
from datetime import datetime

from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


@dataclass
class NewsDay:
    day_iso: str
    news_events : list[NewsEvent]

    def to_dict(self) -> dict:
        return {
            "NewsDay": {
                "day_iso": self.day_iso,
                "news_events": [event.to_dict() for event in self.news_events]
            }
        }



