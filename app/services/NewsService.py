from datetime import datetime

import pytz

from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay


class NewsService:
    def __init__(self):
        self.EconomicScrapper = EconomicScrapper()
        self.newsDays:list[NewsDay] = []
        self.receiveNews()

    def receiveNews(self):
        self.newsDays = self.EconomicScrapper.returnCalendar()

    def isNewsAhead(self,hour:int=1)->bool:
        if len(self.newsDays) == 0:
            raise ValueError

        utc_now = datetime.now(pytz.utc)

        # Convert to UTC-5
        utc_minus_5 = utc_now.astimezone(pytz.timezone('US/Eastern'))  # Eastern Time is UTC-5 during standard time

        for newsDay in self.newsDays:
            day = datetime.fromisoformat(newsDay.dayIso).date().day
            if day == utc_minus_5.day:
                for news in newsDay.newsEvents:
                    if (news.time.hour-hour == utc_minus_5.hour or news.time.hour+hour == utc_minus_5.hour or
                            news.time.hour == utc_minus_5.hour) :
                        return True
        return False
