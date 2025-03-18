import logging

class QueueHandler(logging.Handler):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    def emit(self, record):
        log_entry = self.format(record)
        self.queue.put(log_entry)