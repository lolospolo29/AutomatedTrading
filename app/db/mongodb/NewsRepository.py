from app.db.mongodb.MongoDB import MongoDB
from app.mappers.DTOMapper import DTOMapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class NewsRepository:

    def __init__(self, db_name:str,uri:str):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = DTOMapper()

    # News CRUD

    def add_news_event(self, news_event: NewsEvent):
        news = self._db.find("NewsEvent", {"title": news_event.title,"time": news_event.time})

        if len(news) > 0:
            return
        self._db.add("NewsEvent", news_event.model_dump())

    def add_news_day(self, news_day: NewsDay):
        news = self._db.find("NewsDay", {"day_iso": news_day.day_iso})

        if len(news) > 0:
            return

        self._db.add("NewsDay", news_day.model_dump(exclude={"news_events"}))
