import logging
import queue
import sys
from io import TextIOWrapper
from threading import Thread

from flask import Flask, request, Response, render_template

from Config.Initializing.ClassInstances import signalController

app = Flask(__name__)

# Set up a thread-safe queue for log messages
log_queue = queue.Queue()


# Custom logging handler to put logs into the queue
class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)


# Custom wrapper for stdout and stderr to redirect print statements to the log queue
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


# Set up logging with QueueHandler and redirect stdout/stderr
logger = logging.getLogger()
logger.setLevel(logging.INFO)
queue_handler = QueueHandler()
queue_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(queue_handler)

# Redirect stdout and stderr to log via the StreamToLogger wrapper
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)


@app.route('/tradingview', methods=['POST'])
def receive_signal():
    jsonData = request.get_json()

    # Log received data
    logger.info(f"Received signal data: {jsonData}")

    # Start a thread to process the signal
    thread = Thread(target=signalController.tradingViewSignal, args=(jsonData,))
    thread.start()

    return f'Received Analyse data: {jsonData}'


@app.route('/')
def show_logs():
     return render_template('showLogs.html')

@app.route('/stream')
def stream_logs():
    def generate():
        while True:
            try:
                # Check if there's a log entry available in the queue
                log_entry = log_queue.get(timeout=5)  # Add a timeout to avoid hanging indefinitely when no client is connected
                yield f"data: {log_entry}\n\n"
                log_queue.task_done()
            except queue.Empty:
                continue  # No logs to send, continue waiting

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    

# API Secrets
# Name : DemoApiKey
# API Key : Ifp91Iy8fOY6x22bVG
# Secret: eagubhmZG5nY0gbycEeJNGR50GuT5YnpZA37
