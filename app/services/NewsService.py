import threading
from datetime import datetime, timedelta

import pytz

from app.db.mongodb.NewsRepository import NewsRepository
from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from app.monitoring.logging.logging_startup import logger
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

    def __init__(self,news_repository:NewsRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._economic_scrapper = EconomicScrapper()
            self._news_days: list[NewsDay] = []
            self._news_repository = news_repository
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

        now = datetime.utcnow().isoformat() + "Z"

        # Calculate the date 7 days from now
        future_date = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"

        from_date_iso = datetime.fromisoformat(now.replace("Z", "+00:00"))
        to_date_iso = datetime.fromisoformat(future_date.replace("Z", "+00:00"))

        news_events_db:list[NewsEvent] = self._news_repository.get_news_events(from_date_iso, to_date_iso)
        news_days:list[NewsDay] = self._news_repository.get_news_days(now, future_date)

        for news_day in news_days:

            news_events = []

            for news in news_events_db:
                day = datetime.fromisoformat(news_day.day_iso).date().day
                if day == news.time.day:
                    news_events.append(news)
            news_day.news_events = news_events

        self._news_days = news_days

        logger.debug("News Days received : {count}".format(count=self._news_days))

    def is_news_ahead(self, hour: int = 1) -> tuple[bool, str]:
        """
        Checks if the news day is ahead.

        Returns:
            True if the news day is ahead, False otherwise.
            And the message
        """
        try:
            utc_now = datetime.now(pytz.utc)

            # Convert to UTC-5
            utc_minus_5 = utc_now.astimezone(pytz.timezone('US/Eastern'))  # Eastern Time is UTC-5 during standard time

            for newsDay in self._news_days:
                logger.debug(newsDay.__str__())
                try:
                    day = datetime.fromisoformat(newsDay.day_iso).date().day
                    if day == utc_minus_5.day:
                        for news in newsDay.news_events:
                            logger.debug(news.__str__())
                            if ( news.time.hour - hour == utc_minus_5.hour or news.time.hour + hour == utc_minus_5.hour or
                                    news.time.hour == utc_minus_5.hour):
                                logger.info(f"News Day {newsDay.day_iso} ahead")
                                return True,"News {title}: At {news_hour}".format(title=news.title,news_hour=news.time.hour)
                except Exception as e:
                    logger.critical(f"News Day failed: {e}")
                finally:
                    continue
            return False,""
        except Exception as e:
            logger.critical(e)