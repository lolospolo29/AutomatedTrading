from dataclasses import dataclass
from datetime import datetime

from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


@dataclass
class NewsDay:
    day_iso: str
    news_events : list[NewsEvent]
