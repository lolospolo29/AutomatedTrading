import csv
import json
import os
import shutil
from datetime import datetime

import pandas as pd
from watchdog.events import FileSystemEventHandler

from files.helper.manager.AssetManager import AssetManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.mappers.AssetMapper import AssetMapper
from files.models.asset.Candle import Candle
from files.monitoring.logging.logging_startup import logger
from files.services.BacktestService import BacktestService


class FileHandler(FileSystemEventHandler):
    """
    A singleton class that handles file system events for processing incoming CSV files with TradingView alerts.
    It parses candle data, tests strategies, and organizes processed files into an archive.

    This class uses the Observer pattern to monitor a directory for newly created files and processes them
    as they arrive, integrating with `AssetManager` and `StrategyManager`.
    """
    # region Initializing

    def __init__(self, asset_manager:AssetManager, strategy_manager:StrategyRegistry, backtest_service:BacktestService):
        self._asset_manager: AssetManager = asset_manager
        self._strategy_manager: StrategyRegistry = strategy_manager
        self._backtest_service:BacktestService = backtest_service

    # endregion

    # region Watcher
    def on_created(self, event):
        """
            Handles file creation events in the monitored directory. Processes new CSV files that match
            TradingView alert log naming patterns by parsing candle data, testing strategies, and moving
            processed files to the archive.

            Args:
                event: The event triggered by the file system when a new file is created.
            """
        try:
            logger.debug("Processed File {}".format(event.src_path))
            filename = os.path.basename(event.src_path)
            logger.info("Processing file {}".format(filename))

            if filename.startswith("TradingView_Alerts_Log") and filename.endswith(".csv"):

                candles_dict_list = self._parse_candle_data(event.src_path)

                logger.debug("Candles list {}".format(len(candles_dict_list)))

                for candle_dict in candles_dict_list:
                    try:
                        candle:Candle = AssetMapper().map_tradingview_json_to_candle(candle_dict)
                        candle: Candle = self._asset_manager.add_candle(candle)
                    except Exception as e:
                        logger.debug("Failed to add Candle to AssetManager from File: {}".format(e))
                    finally:
                        continue
            if filename.startswith("Testdata") and filename.endswith(".csv"):
                candles_dict_list = self._parse_candle_data(event.src_path)
                candles = []
                for candle_dict in candles_dict_list:
                    try:
                        candle:Candle = AssetMapper().map_tradingview_json_to_candle(candle_dict)
                        candles.append(candle)
                    except Exception as e:
                        logger.debug("Failed to add Candle to AssetManager from File: {}".format(e))
                self._backtest_service.add_test_data(candles)
            self._move_to_archive(event.src_path)
        except Exception as e:
            logger.error("Failed to add Candle to AssetManager from File: {}".format(e))
    # endregion

    # region CSV Parsing
    def candle_csv_to_backtest_db(self, folder_path):
        candles = self._read_from_multiple_candle_files(folder_path)
        self._backtest_service.add_test_data(candles)

    @staticmethod
    def _read_from_multiple_candle_files(folder_path):
        candles = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    parts = file.split(".")[0]  # Entfernt die Dateiendung
                    asset = "".join(filter(str.isalpha, parts))  # Extrahiert den Asset-Namen
                    timeframe = int("".join(filter(str.isdigit, parts)))  # Extrahiert die Zahl als Timeframe

                    df = pd.read_csv(file_path, delimiter='\t', header=None,
                                     names=["iso_time", "open", "high", "low", "close", "volume"])

                    for _, row in df.iterrows():
                        candle = Candle(
                            asset=asset,
                            broker="Faker",
                            open=row["open"],
                            high=row["high"],
                            low=row["low"],
                            close=row["close"],
                            iso_time=datetime.strptime(row["iso_time"], "%Y-%m-%d %H:%M"),
                            timeframe=timeframe
                        )
                        candles.append(candle)


        return candles


    @staticmethod
    def _parse_candle_data(csv_filename) -> list[dict]:
        """Parses the Candle Data from a TradingView CSV"""
        candles = []
        try:
            with open(csv_filename, mode='r', newline='') as file:
                reader = list(csv.DictReader(file))
                description_keys = ["Beschreibung", "Description", "Descripción", "Descrizione", "Описание", "描述"]

                for row in reversed(reader):
                    # change back to normal after debug reversed
                    beschreibung_text = None
                    for key in description_keys:
                        if key in row:  # Prüfe, ob die Spalte existiert
                            beschreibung_text = row[key]
                            break  # Erste gefundene Beschreibung verwenden

                    if beschreibung_text is None:
                        print("Keine passende Spalte für die Beschreibung gefunden.")
                        continue  # Überspringen, wenn keine Beschreibung gefunden wurde

                    # JSON parsen
                    description_json = json.loads(beschreibung_text)


                    # candle_data = description_json["Candle"]
                    candle_data = description_json.get("Candle", {})

                    # Structure candle data to match the desired output format
                    formatted_candle = {
                        'Candle': {
                            'iso_time': candle_data.get('iso_time', ''),
                            'asset': candle_data.get('asset', ''),
                            'broker': candle_data.get('broker', ''),
                            'close': float(candle_data.get('close', 0.0)),
                            'high': float(candle_data.get('high', 0.0)),
                            'low': float(candle_data.get('low', 0.0)),
                            'open': float(candle_data.get('open', 0.0)),
                            'timeframe': int(candle_data.get('timeframe', 0))
                        }
                    }
                    candles.append(formatted_candle)
            return candles
        except Exception as e:
            logger.error("Failed to Parse Candle Data from CSV: {e}".format(e=e))
            return candles

    # endregion

    # region File Functions

    @staticmethod
    def _delete_file(file_path):
        try:
            # Delete the file after processing
            os.remove(file_path)
            logger.info(f"Deleted File: {file_path}")

        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def _move_to_archive(src_path):
        try:
            # Get the directory where the source file is located
            src_dir = os.path.dirname(src_path)

            # Define the _archive folder path within the same directory
            archive_folder = os.path.join(src_dir, "_archive")

            # Ensure the _archive folder exists, create it if it doesn't
            if not os.path.exists(archive_folder):
                os.makedirs(archive_folder)

            # Define the destination path for the file inside the _archive folder
            destination = os.path.join(archive_folder, os.path.basename(src_path))

            # Move the file to the _archive folder
            shutil.move(src_path, destination)
            logger.info(f"File moved to _archive: {destination}")

        except Exception as e:
            logger.error(f"Error moving file {src_path} to _archive: {e}")
    # endregion
