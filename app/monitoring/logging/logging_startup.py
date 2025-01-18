import logging
import queue
import sys
from io import TextIOWrapper

from app.monitoring.logging.CSVFileHandler import CSVFileHandler

import logging

class StreamToLogger(TextIOWrapper):
    def __init__(self, logger, level=logging.INFO):
        super().__init__(sys.stdout.buffer, write_through=True)
        self.logger = logger
        self.level = level


    def write(self, message):
        if message.strip():  # Avoid blank lines
            self.logger.log(self.level, message)

    def flush(self):
        pass  # No action needed for flush, as logging handles it

class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)

log_queue = queue.Queue()

# Set up logging with QueueHandler and redirect stdout/stderr
logger = logging.getLogger()
logger.setLevel(logging.INFO)
queue_handler = QueueHandler()
queue_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(queue_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
# Add CSVFileHandler to write logs to a CSV file
csv_handler = CSVFileHandler('logs.csv')
csv_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(csv_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)