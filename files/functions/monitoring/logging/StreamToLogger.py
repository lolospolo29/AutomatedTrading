import logging
import sys
from io import TextIOWrapper


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