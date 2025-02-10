from datetime import datetime

from pydantic import BaseModel


class NewsEvent(BaseModel):
    """
    Represents a news event with its details, typically used in financial or economic contexts.

    This class models an event typically reported in news, especially those with economic relevance.
    It includes the details of the event time, title, associated currency, and the time of day when
    the event occurs. Instances of this class can be utilized to track or analyze such events.

    """
    time: datetime # 7:00 for example or 1:12
    title: str # Example:Nonfarm PayRoll
    currency:str # US
    daytime:str # AM or PM
