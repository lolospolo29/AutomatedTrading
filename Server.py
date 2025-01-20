import queue
from threading import Thread

from flask import Flask, request, Response, render_template

from app.ClassInstances import signal_controller
from app.monitoring.logging.logging_startup import logger, log_queue

app = Flask(__name__)

@app.route('/tradingview', methods=['post'])
def receive_signal():
    json_data = request.get_json()

    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=signal_controller.trading_view_signal, args=(json_data,))
    thread.start()

    return f'Received Analyse data: {json_data}'


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
