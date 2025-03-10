import queue
import sys
from io import TextIOWrapper

import logging

import requests

class StreamToLogger(TextIOWrapper):
    def __init__(self, logger_instance, level=logging.INFO):
        super().__init__(sys.stdout.buffer, write_through=True)
        self.logger = logger_instance
        self.level = level

    def write(self, message):
        if message.strip():  # Avoid blank lines
            self.logger.log(self.level, message)

    def flush(self):
        pass  # No action needed for flush, as logging handles it

class HTTPLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        requests.post("https://dein-log-server.com/logs", json={"log": log_entry})

class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)

log_queue = queue.Queue()

#http_logger = HTTPLogHandler()
queue_handler = QueueHandler()

logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)
#http_logger.setLevel(logging.INFO)

queue_handler.setFormatter(formatter)
#http_logger.setFormatter(formatter)
#logger.addHandler(http_logger)
logger.addHandler(queue_handler)


# Redirect stdout and stderr to log via the StreamToLogger wrapper
# Add CSVFileHandler to write logs to a CSV file
#csv_handler = CSVFileHandler('logs.csv')
#csv_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
#logger.addHandler(csv_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
#sys.stdout = StreamToLogger(logger, logging.INFO)
#sys.stderr = StreamToLogger(logger, logging.ERROR)