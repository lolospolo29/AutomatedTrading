from dataclasses import dataclass
from datetime import datetime

from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


@dataclass
class NewsDay:
    dayIso: datetime
    newsEvents : list[NewsEvent]
