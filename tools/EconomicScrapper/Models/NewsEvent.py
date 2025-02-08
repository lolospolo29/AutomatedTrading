from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsEvent:
    time: datetime # 7:00 for example or 1:12
    title: str # Example:Nonfarm PayRoll
    currency:str # US
    daytime:str # AM or PM

    def to_dict(self) -> dict:
        return {
            "time": self.time.strftime("%I:%M"),  # Formatting time to match the example
            "title": self.title,
            "currency": self.currency,
            "daytime": self.daytime
        }
