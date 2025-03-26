import threading
from datetime import datetime, timedelta, timezone
from logging import Logger

import pytz

from files.db.repositories.NewsRepository import NewsRepository
from files.helper.functions.to_utc import to_utc
from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent

class NewsService:
    """
    Handles operations related to economic news, including receiving and analyzing news days.

    This class interacts with an economic scrapper to receive news events and determine if any
    relevant news is ahead within a specified timeframe.

    :ivar _economic_scrapper: An instance of the EconomicScrapper used to fetch economic news data.
    :type _economic_scrapper: EconomicScrapper
    :ivar _news_days: A list holding news days and their corresponding news events.
    :type _news_days: list[NewsDay]
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(NewsService, cls).__new__(cls)
        return cls._instance

    def __init__(self,news_repository:NewsRepository,economic_scrapper:EconomicScrapper
                 ,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._economic_scrapper = economic_scrapper
            self._news_days: list[NewsDay] = []
            self._news_repository = news_repository
            self.logger = logger
            self._initialized = True  # Markiere als initialisiert

    def run_news_scheduler(self):
        self._news_days = self._economic_scrapper.return_calendar()
        for newsDay in self._news_days:
            self._news_repository.add_news_day(newsDay)
            for news in newsDay.news_events:
                self._news_repository.add_news_event(news)

    def return_news_days(self)->list[NewsDay]:
        return self._news_days

    def fetch_news(self):
        """
        Receiving the News from Scrapper.

        Returns:
            Safe News on the Day to the List.
        """

        now = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

        # Calculate the date 7 days from now and set the time to 00:00:00
        future_date = (datetime.utcnow() + timedelta(days=7)).replace(hour=0, minute=0, second=0,
                                                                      microsecond=0).isoformat()
        from_date_iso = datetime.fromisoformat(now.replace("Z", "+00:00"))
        to_date_iso = datetime.fromisoformat(future_date.replace("Z", "+00:00"))

        time_obj = from_date_iso.replace(tzinfo=timezone.utc)
        from_date_iso = to_utc(time_obj)

        time_obj = to_date_iso.replace(tzinfo=timezone.utc)
        to_date_iso = to_utc(time_obj)

        news_events_db:list[NewsEvent] = self._news_repository.get_news_events(from_date_iso, to_date_iso)
        news_days:list[NewsDay] = self._news_repository.get_news_days(from_date_iso, to_date_iso)

        for news_day in news_days:

            news_events = []

            for news in news_events_db:
                day = news_day.day_iso.day
                if day == news.time.day:
                    news_events.append(news)
            news_day.news_events = news_events

        self._news_days = news_days

        self.logger.debug("News Days received : {count}".format(count=self._news_days))

    def is_news_ahead(self, hour: int = 1) -> tuple[bool, str]:
        """
        Checks if the news day is ahead.

        Returns:
            True if the news day is ahead, False otherwise.
            And the message
        """
        try:
            utc_now = datetime.now(pytz.utc)

            for newsDay in self._news_days:
                self.logger.debug(newsDay.__str__())
                try:
                    day = newsDay.day_iso.day
                    if day == utc_now.day:
                        for news in newsDay.news_events:
                            self.logger.debug(news.__str__())
                            if ( news.time.hour - hour == utc_now.hour or news.time.hour + hour == utc_now.hour or
                                    news.time.hour == utc_now.hour):
                                self.logger.info(f"News Day {newsDay.day_iso} ahead")
                                return True,"News {title}: At {news_hour}".format(title=news.title,news_hour=news.time.hour)
                except Exception as e:
                    self.logger.critical(f"News Day failed: {e}")
            return False,""
        except Exception as e:
            self.logger.critical(e)