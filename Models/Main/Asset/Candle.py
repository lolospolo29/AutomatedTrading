from datetime import datetime

from Models.Pattern.Decorator.IDDecorator import IDDecorator
from Models.Pattern.Factory.FlyweightFactory import FlyweightFactory


@IDDecorator
class Candle:
    def __init__(self, asset: str, broker: str, open: float, high: float, low: float, close: float,
                 IsoTime: datetime, timeFrame: int):
        self.asset: str = FlyweightFactory.getFlyweight(asset)
        self.broker: str = FlyweightFactory.getFlyweight(broker)
        self.open: float = FlyweightFactory.getFlyweight(open)
        self.high: float = FlyweightFactory.getFlyweight(high)
        self.low: float = FlyweightFactory.getFlyweight(low)
        self.close: float = FlyweightFactory.getFlyweight(close)

        # Konvertiere oder validiere IsoTime
        if isinstance(IsoTime, str):
            try:
                self.isoTime: datetime = datetime.strptime(IsoTime, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValueError(f"Invalid ISO time format: {IsoTime}")
        elif isinstance(IsoTime, datetime):
            self.isoTime = IsoTime
        else:
            raise TypeError(f"IsoTime must be a string or datetime, got {type(IsoTime).__name__}")

        self.timeFrame: int = FlyweightFactory.getFlyweight(timeFrame)

        print(f"Type of isoTime: {type(self.isoTime)}")  # Erwartet: <class 'datetime.datetime'>

    def toDict(self) -> dict:
        """Gibt alle Datenpunkte als Dictionary zurück"""
        return {
            "Candle": {
                "asset": self.asset,
                "broker": self.broker,
                "open": self.open,
                "high": self.high,
                "low": self.low,
                "close": self.close,
                "IsoTime": self.isoTime,  # In ISO 8601-String konvertieren
                "timeFrame": self.timeFrame
            }
        }
