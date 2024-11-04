import datetime


class Candle:
    def __init__(self, broker: str, asset: str, open: float, high: float, low: float, close: float,
                 IsoTime: datetime, timeFrame: int):
        self.asset: str = asset
        self.broker: str = broker
        self.open: float = open
        self.high: float = high
        self.low: float= low
        self.close: float = close
        self.isoTime: datetime = IsoTime
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
                "close": self.close,
                "IsoTime": self.isoTime,  # Formatiert nur die Uhrzeit
                "timeFrame": self.timeFrame  # Zeitstempel im Format ISO
            }
        }
