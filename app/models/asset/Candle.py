import uuid
from datetime import datetime

class Candle:

    def __init__(self, asset: str, broker: str, open: float, high: float, low: float, close: float,
                 iso_time: datetime, timeframe: int, id:str=None):
            self.asset: str = asset
            self.broker: str = broker
            self.open: float = open
            self.high: float = high
            self.low: float = low
            self.close: float = close
            if id is None:
                self.id: str = str(uuid.uuid4())

            # Konvertiere oder validiere IsoTime
            if isinstance(iso_time, str):
                try:
                    self.iso_time: datetime = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    raise ValueError(f"Invalid ISO time format: {iso_time}")
            elif isinstance(iso_time, datetime):
                self.iso_time = iso_time
            else:
                raise TypeError(f"IsoTime must be a string or datetime, got {type(iso_time).__name__}")

            self.timeframe: int = timeframe


    def to_dict(self) -> dict:
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
                "iso_time": self.iso_time,  # In ISO 8601-String konvertieren
                "timeframe": self.timeframe
            }
        }
