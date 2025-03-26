import logging
import csv
from datetime import datetime

class CSVFileHandler(logging.Handler):
    """
    Custom logging handler to write logs into a CSV file.
    """
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

        # Write the header row if the file doesn't exist or is empty
        try:
            with open(self.filename, mode='r') as f:
                if not f.readline():
                    self._write_header()
        except FileNotFoundError:
            self._write_header()

    def _write_header(self):
            """Write the CSV header row."""
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Level", "Message", "Timestamp"])

    def emit(self, record):
        """Write a log record to the CSV file."""
        # Create a timestamp manually
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write the log record to the CSV file
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([record.levelname, record.msg, timestamp])
