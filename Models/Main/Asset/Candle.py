import datetime

from Models.Pattern.Factory.FlyweightFactory import FlyweightFactory


class Candle:
    def __init__(self, broker: str, asset: str, open: float, high: float, low: float, close: float,
                 IsoTime: datetime, timeFrame: int):
        self.asset: str = FlyweightFactory.getFlyweight(asset)
        self.broker: str = FlyweightFactory.getFlyweight(broker)
        self.open: float = FlyweightFactory.getFlyweight(open)
        self.high: float = FlyweightFactory.getFlyweight(high)
        self.low: float= FlyweightFactory.getFlyweight(low)
        self.close: float = FlyweightFactory.getFlyweight(close)
        self.isoTime: datetime = IsoTime
        self.timeFrame: int = FlyweightFactory.getFlyweight(timeFrame)

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
                "IsoTime": self.isoTime,  # Formatiert nur die Uhrzeit
                "timeFrame": self.timeFrame  # Zeitstempel im Format ISO
            }
        }
