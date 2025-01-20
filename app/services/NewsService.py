from datetime import datetime

import pytz

from tools.EconomicScrapper.EconomicScrapper import EconomicScrapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from app.monitoring.logging.logging_startup import logger


class NewsService:
    """Uses the EconomicScrapper to scrap news articles and store them in the List"""

    def __init__(self):
        self.economic_scrapper = EconomicScrapper()
        self.news_days: list[NewsDay] = []
        self.logger = logger

    def receive_news(self):
        """
        Receiving the News from Scrapper.

        Returns:
            Safe News on the Day to the List.
        """
        self.logger.info("Receiving News from Scrapper.")
        self.news_days = self.economic_scrapper.return_calendar()
        self.logger.info("News Days received : {count}".format(count=self.news_days))

    def is_news_ahead(self, hour: int = 1) -> bool:
        """
        Checks if the news day is ahead.

        Returns:
            True if the news day is ahead, False otherwise.
        """
        try:
            utc_now = datetime.now(pytz.utc)

            # Convert to UTC-5
            utc_minus_5 = utc_now.astimezone(pytz.timezone('US/Eastern'))  # Eastern Time is UTC-5 during standard time

            for newsDay in self.news_days:
                self.logger.debug(newsDay.__str__())
                try:
                    day = datetime.fromisoformat(newsDay.day_iso).date().day
                    if day == utc_minus_5.day:
                        for news in newsDay.news_events:
                            logger.debug(news.__str__())
                            if (
                                    news.time.hour - hour == utc_minus_5.hour or news.time.hour + hour == utc_minus_5.hour or
                                    news.time.hour == utc_minus_5.hour):
                                self.logger.info(f"News Day {newsDay.day_iso} ahead")
                                return True
                except Exception as e:
                    logger.critical(f"News Day failed: {e}")
                finally:
                    continue
            return False
        except Exception as e:
            self.logger.critical(e)
