import threading

from app.db.mongodb.MongoDB import MongoDB
from app.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from app.manager.initializer.SecretsManager import SecretsManager
from app.mappers.DTOMapper import DTOMapper
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class NewsRepository:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(NewsRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._secret_manager: SecretsManager = SecretsManager()
            self.__secret = self._secret_manager.return_secret("mongodb")
            self._dto_mapper = DTOMapper()
            self._initialized = True  # Markiere als initialisiert

    # News CRUD

    def add_news_event(self, news_event: NewsEvent):
        db = MongoDB(dbName="News",uri= self.__secret)

        news = db.find("NewsEvent", {"title": news_event.title,"time": news_event.time})

        if len(news) > 0:
            return
        db.add("NewsEvent", news_event.model_dump())

    def add_news_day(self, news_day: NewsDay):
        db = MongoDB(dbName="News",uri= self.__secret)
        news = db.find("NewsDay", {"day_iso": news_day.day_iso})

        if len(news) > 0:
            return

        db.add("NewsDay", news_day.model_dump(exclude={"news_events"}))
