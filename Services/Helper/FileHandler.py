import csv
import json
import os
import shutil
from datetime import datetime

import pandas as pd
from watchdog.events import FileSystemEventHandler

from Initializing.GlobalStatements import setLockState, getLockState
from Monitoring.TimeWrapper import logTime
from Services.Manager.AssetManager import AssetManager
from Services.Manager.StrategyManager import StrategyManager


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, assetManager: AssetManager, strategyManager: StrategyManager):
        self._AssetManager: AssetManager = assetManager
        self._StrategyManager: StrategyManager = strategyManager

    @logTime
    def on_created(self, event):
        # Only process the specific file name

        if not getLockState():
            setLockState(True)
            filename = os.path.basename(event.src_path)

            if filename.startswith("TradingView_Alerts_Log") and filename.endswith(".csv"):
                print(f"New file detected: {event.src_path}")
                candlesCSV = self.parseCandleData(event.src_path)
                for candle in candlesCSV:
                    asset, broker, timeFrame = self._AssetManager.addCandle(candle)
                    candles: list = self._AssetManager.returnCandles(asset, broker, timeFrame)
                    relations: list = self._AssetManager.returnRelations(asset, broker)
                    for relation in relations:
                        self._StrategyManager.analyzeStrategy(candles, relation,timeFrame)

                        _ids = [candle.id for candle in candles]
                        self._StrategyManager.updateFrameWorkHandler(_ids, relation, timeFrame)

                        self._StrategyManager.getEntry(candles, relation, timeFrame)

                self.moveToArchive(event.src_path)
                self.archive()
                setLockState(False)

    @staticmethod
    def parseCandleData(csv_filename) -> list:
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

    @staticmethod
    def archive():

        # Pfade definieren
        observed_folder = r"C:\AutomatedTrading\ObservedFolder\archive"
        # Sicherstellen, dass der Archivordner existiert

        # Alle Dateien im ObservedFolder iterieren
        # Alle Dateien im ObservedFolder iterieren
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

            # Daten nach Asset-Typ und Datum filtern
            for _, row in data.iterrows():
                try:
                    # JSON aus der "Description"-Spalte extrahieren
                    description_json = row["Description"]
                    candle_data = json.loads(description_json)
                    asset = candle_data["Candle"]["asset"]
                    iso_time = candle_data["Candle"]["IsoTime"]

                    # Datum aus IsoTime extrahieren
                    date = datetime.strptime(iso_time.rstrip("Z"), "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')

                    # Ordnerstruktur: archive/<asset>/<date>
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
    def deleteFile(file_path):
        try:
            # Delete the file after processing
            os.remove(file_path)
            print(f"File deleted: {file_path}")

        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def moveToArchive(src_path):
        try:
            # Get the directory where the source file is located
            src_dir = os.path.dirname(src_path)

            # Define the archive folder path within the same directory
            archive_folder = os.path.join(src_dir, "archive")

            # Ensure the archive folder exists, create it if it doesn't
            if not os.path.exists(archive_folder):
                os.makedirs(archive_folder)

            # Define the destination path for the file inside the archive folder
            destination = os.path.join(archive_folder, os.path.basename(src_path))

            # Move the file to the archive folder
            shutil.move(src_path, destination)
            print(f"File moved to archive: {destination}")

        except Exception as e:
            print(f"Error moving file {src_path}: {e}")