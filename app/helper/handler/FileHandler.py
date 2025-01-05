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


class FileHandler(FileSystemEventHandler):

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(FileHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._AssetManager: AssetManager = AssetManager()
            self._StrategyManager: StrategyManager = StrategyManager()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Watcher
    def on_created(self, event):
        # Only process the specific file name

            filename = os.path.basename(event.src_path)

            if filename.startswith("TradingView_Alerts_Log") and filename.endswith(".csv"):
                print(f"New file detected: {event.src_path}")
                self._StrategyManager.setLockWithTimeout()
                candlesCSV = self._parseCandleData(event.src_path)
                for candle in candlesCSV:
                    candle: Candle = self._AssetManager.addCandle(candle)
                    self._testingStrategy(candle.asset, candle.broker, candle.timeFrame)

                self._moveToArchive(event.src_path)
                self._archive()

    def _testingStrategy(self, asset, broker, timeFrame):
        candles: list[Candle] = self._AssetManager.returnCandles(asset, broker, timeFrame)
        relations: list = self._AssetManager.returnRelations(asset, broker)
        for relation in relations:
            self._StrategyManager.analyzeStrategy(candles, relation, timeFrame)

    # endregion

    # region CSV Parsing
    @staticmethod
    def _parseCandleData(csv_filename) -> list:
        candles = []
        with open(csv_filename, mode='r', newline='') as file:
            reader = list(csv.DictReader(file))

            for row in reversed(reader): # change back to normal after debug reversed
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

            print(f"Verarbeite Datei: {filename}")

            # CSV-Datei einlesen
            try:
                data = pd.read_csv(file_path)
            except Exception as e:
                print(f"Fehler beim Einlesen von {filename}: {e}")
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
                    with open(asset_file_path, "a") as f:
                        f.write(",".join(map(str, row.values)) + "\n")  # Originalzeile speichern
                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Zeile in {filename}: {e}")
                    continue

            print(f"Verarbeitung von {filename} abgeschlossen.")

    @staticmethod
    def _deleteFile(file_path):
        try:
            # Delete the file after processing
            os.remove(file_path)
            print(f"File deleted: {file_path}")

        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def _moveToArchive(src_path):
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
            print(f"File moved to _archive: {destination}")

        except Exception as e:
            print(f"Error moving file {src_path}: {e}")
    # endregion