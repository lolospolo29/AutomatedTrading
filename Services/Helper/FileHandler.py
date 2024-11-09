import csv
import json
import os
import shutil

from watchdog.events import FileSystemEventHandler

from Initializing.GlobalStatements import set_lock_state, get_lock_state
from Services.Manager.AssetManager import AssetManager


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, assetManager: AssetManager):
        self._AssetManager: AssetManager = assetManager

    def on_created(self, event):
        # Only process the specific file name
        set_lock_state(True)
        if not get_lock_state():
            filename = os.path.basename(event.src_path)
            if filename.startswith("TradingView_Alerts_Log") and filename.endswith(".csv"):
                print(f"New file detected: {event.src_path}")
                candles = self.parseCandleData(event.src_path)
                for candle in candles:
                    self._AssetManager.addCandle(candle)

                self.moveToArchive(event.src_path)
                set_lock_state(False)

    @staticmethod
    def parseCandleData(csv_filename) -> list:
        candles = []
        with open(csv_filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
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