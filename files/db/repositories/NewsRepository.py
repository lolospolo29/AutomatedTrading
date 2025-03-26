from datetime import datetime

from files.db.MongoDB import MongoDB
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class NewsRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region News

    def add_news_event(self, news_event: NewsEvent):
        self._db.add("NewsEvent", news_event.model_dump(exclude={"_id"}))

    def add_news_day(self, news_day: NewsDay):
        self._db.add("NewsDay", news_day.model_dump(exclude={"_id"}))

    def get_news_events(self, from_date: datetime, to_date: datetime)->list[NewsEvent]:
        news_events = []

        # MongoDB-Abfrage mit Datumsbereich auf das Feld "time"
        query = {"time": {"$gte": from_date, "$lte": to_date}}

        # Datenbankabfrage
        news_db = self._db.find("NewsEvent", query)

        # Ergebnisse verarbeiten
        for news_event in news_db:
            news_event.pop("_id", None)  # Remove _id if it exists
            news_events.append(NewsEvent.model_validate(news_event))

        return news_events

    def get_news_days(self, from_date: datetime, to_date: datetime)->list[NewsDay]:
        news_days = []

        # MongoDB-Abfrage mit Datumsbereich auf das Feld "time"
        query = {
            "day_iso": {
                "$gte": from_date,  # Start date (inclusive) - formatted as 'YYYY-MM-DD'
                "$lte": to_date  # End date (inclusive) - formatted as 'YYYY-MM-DD'
            }
        }
        # Datenbankabfrage
        news_db = self._db.find("NewsDay", query)

        # Ergebnisse verarbeiten
        for news_event in news_db:
            news_event.pop("_id", None)  # Remove _id if it exists
            news_days.append(NewsDay.model_validate(news_event))

        return news_days
    # endregion