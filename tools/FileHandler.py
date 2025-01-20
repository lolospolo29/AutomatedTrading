import csv
import json
import os
import shutil
import threading
from datetime import datetime

import pandas as pd
from watchdog.events import FileSystemEventHandler

from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.models.asset.Candle import Candle
from app.monitoring.logging.logging_startup import logger


class FileHandler(FileSystemEventHandler):
    """
    A singleton class that handles file system events for processing incoming CSV files with TradingView alerts.
    It parses candle data, tests strategies, and organizes processed files into an archive.

    This class uses the Observer pattern to monitor a directory for newly created files and processes them
    as they arrive, integrating with `AssetManager` and `StrategyManager`.
    """
    # region Initializing

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(FileHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._asset_manager: AssetManager = AssetManager()
            self._strategy_manager: StrategyManager = StrategyManager()
            self._initialized = True  # Markiere als initialisiert

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
                            candle: Candle = self._asset_manager.add_candle(candle_dict)
                            self._testing_strategy(candle.asset, candle.broker, candle.timeframe)
                        except Exception as e:
                            logger.error("Failed to add Candle to AssetManager from File: {}".format(e))
                        finally:
                            continue

                    self._move_to_archive(event.src_path)
                    self._archive()
            except Exception as e:
                logger.error("Failed to add Candle to AssetManager from File: {}".format(e))

    def _testing_strategy(self, asset, broker, timeFrame):
        try:
            candles: list[Candle] = self._asset_manager.return_candles(asset, broker, timeFrame)
            relations: list = self._asset_manager.return_relations(asset, broker)
            for relation in relations:
                try:
                    logger.debug("Processing Entries for {}".format(relation))
                    self._strategy_manager.get_entry(candles, relation, timeFrame)
                except Exception as e:
                    logger.error("Failed to Analyze Strategy Manager: {}".format(e))
                finally:
                    continue
        except Exception as e:
            logger.error("Testing strategy failed for asset: {}".format(asset))

    # endregion

    # region CSV Parsing
    @staticmethod
    def _parse_candle_data(csv_filename) -> list[dict]:
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
                                'iso_time': candle_data.get('IsoTime', ''),
                                'asset': candle_data.get('asset', ''),
                                'broker': candle_data.get('broker', ''),
                                'close': float(candle_data.get('close', 0.0)),
                                'high': float(candle_data.get('high', 0.0)),
                                'low': float(candle_data.get('low', 0.0)),
                                'open': float(candle_data.get('open', 0.0)),
                                'timeframe': int(candle_data.get('timeFrame', 0))
                            }
                        }
                        candles.append(formatted_candle)
            return candles
        except Exception as e:
            logger.error("Failed to Parse Candle Data from CSV: {e}".format(e=e))
    # endregion

    # region File Functions
    @staticmethod
    def _archive():

        # Pfade definieren
        observed_folder = r"/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles/_archive"
        # Sicherstellen, dass der Archivordner existiert

        # Alle Dateien im incomingFiles iterieren
        for filename in os.listdir(observed_folder):
            file_path = os.path.join(observed_folder, filename)

            # Nur CSV-Dateien verarbeiten
            if not filename.endswith(".csv"):
                continue

            logger.info(f"Verarbeite Datei: {filename}")

            # CSV-Datei einlesen
            try:
                data = pd.read_csv(file_path)
            except Exception as e:
                logger.exception(f"Fehler beim Einlesen von {filename}: {e}")
                continue

            # Daten nach asset-Typ und Datum filtern
            for _, row in data.iterrows():
                try:
                    # JSON aus der "Description"-Spalte extrahieren
                    description_json = row["Description"]
                    candle_data = json.loads(description_json)
                    asset = candle_data["Candle"]["asset"]
                    iso_time = candle_data["Candle"]["IsoTime"]

                    # Datum aus IsoTime extrahieren
                    date = datetime.strptime(iso_time.rstrip("Z"), "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')

                    # Ordnerstruktur: _archive/<asset>/<date>
                    asset_folder = os.path.join(observed_folder, asset, date)
                    os.makedirs(asset_folder, exist_ok=True)

                    # Datei für das Datum erstellen oder anhängen
                    asset_file_path = os.path.join(asset_folder, f"{asset}_{date}.csv")
                    logger.debug(f"Writing to {asset_file_path}")
                    with open(asset_file_path, "a") as f:
                        f.write(",".join(map(str, row.values)) + "\n")  # Originalzeile speichern
                except Exception as e:
                    logger.error(f"Error Writing to: {filename}: {e}")
                    continue

            logger.info(f"Succeed :{filename}.")

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
