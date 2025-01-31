import csv
import json

from app.mappers.exceptions.MappingFailedExceptionError import MappingFailedExceptionError
from app.models.asset.Candle import Candle
from app.monitoring.logging.logging_startup import logger


class AssetMapper:
    """Maps the Candles from TradingView"""
    @staticmethod
    def parse_candle_data(csv_filename="/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles/TradingView_Alerts_Log_2025-01-05.csv") -> list[dict]:
        """Parses the Candle Data from a TradingView CSV"""
        candles = []
        try:
            with open(csv_filename, mode='r', newline='') as file:
                reader = list(csv.DictReader(file))

                for row in reversed(reader):
                        # change back to normal after debug reversed
                        description_json = json.loads(row["Description"])
                        # candle_data = description_json["Candle"]
                        candle_data = description_json.get("Candle", {})

                        # Structure candle data to match the desired output format
                        formatted_candle = {
                            'Candle': {
                                'IsoTime': candle_data.get('IsoTime', ''),
                                'asset': candle_data.get('asset', ''),
                                'broker': candle_data.get('broker', ''),
                                'close': float(candle_data.get('close', 0.0)),
                                'high': float(candle_data.get('high', 0.0)),
                                'low': float(candle_data.get('low', 0.0)),
                                'open': float(candle_data.get('open', 0.0)),
                                'timeFrame': int(candle_data.get('timeFrame', 0))
                            }
                        }
                        candles.append(formatted_candle)
            return candles
        except Exception as e:
            logger.error("Failed to Parse Candle Data from CSV: {e}".format(e=e))

    @staticmethod
    def map_candle_from_trading_view(json: dict) -> Candle:
        """
        Updates the attributes of a regular class instance with values from a dataclass instance.

        Args:
            json: json from Tradingview

        Returns:
            Candle for Asset.
        """
        try:
            logger.debug(json)
            candle = json.get("Candle")
            asset = candle.get("asset")
            broker = candle.get("broker")
            open = candle.get("open")
            close = candle.get("close")
            high = candle.get("high")
            low = candle.get("low")
            iso_time = candle.get("iso_time")
            timeFrame = candle.get("timeframe")
            return Candle(asset, broker, open, high, low, close, iso_time, timeFrame)
        except Exception as e:
            raise MappingFailedExceptionError("Candle")
