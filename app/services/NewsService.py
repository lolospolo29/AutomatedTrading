from datetime import datetime

import pytz

from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay


class NewsService:
    def __init__(self):
        self.economic_scrapper = EconomicScrapper()
        self.news_days:list[NewsDay] = []
        self.receive_news()

    def receive_news(self):
        self.news_days = self.economic_scrapper.return_calendar()

    def is_news_ahead(self, hour:int=1)->bool:
        if len(self.news_days) == 0:
            raise ValueError

        utc_now = datetime.now(pytz.utc)

        # Convert to UTC-5
        utc_minus_5 = utc_now.astimezone(pytz.timezone('US/Eastern'))  # Eastern Time is UTC-5 during standard time

        for newsDay in self.news_days:
            day = datetime.fromisoformat(newsDay.day_iso).date().day
            if day == utc_minus_5.day:
                for news in newsDay.news_events:
                    if (news.time.hour-hour == utc_minus_5.hour or news.time.hour+hour == utc_minus_5.hour or
                            news.time.hour == utc_minus_5.hour) :
                        return True
        return False
