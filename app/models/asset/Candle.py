import uuid
from datetime import datetime

class Candle:

    def __init__(self, asset: str, broker: str, open: float, high: float, low: float, close: float,
                 IsoTime: datetime, timeFrame: int,id:str=None):
        self.asset: str = asset
        self.broker: str = broker
        self.open: float = open
        self.high: float = high
        self.low: float = low
        self.close: float = close
        if id is None:
            self.id: str = str(uuid.uuid4())

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

        self.timeFrame: int = timeFrame

    def toDict(self) -> dict:
        """Gibt alle Datenpunkte als Dictionary zurück"""
        return {
            "Candle": {
                "asset": self.asset,
                "broker": self.broker,
                "open": self.open,
                "high": self.high,
                "low": self.low,
                "id":self.id,
                "close": self.close,
                "IsoTime": self.isoTime,  # In ISO 8601-String konvertieren
                "timeFrame": self.timeFrame
            }
        }
