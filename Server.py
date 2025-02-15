import queue
from threading import Thread

from flask import Flask, request, Response, render_template, jsonify

from app.ClassInstances import signal_controller
from app.monitoring.logging.logging_startup import logger, log_queue

app = Flask(__name__)
# region POST APP Route
@app.route('/tradingview', methods=['post'])
def receive_signal():
    json_data = request.get_json()

    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=signal_controller.trading_view_signal, args=(json_data,))
    thread.start()

    return f'Received Analyse data: {json_data}'

@app.route('/delete-asset', methods=['POST'])
def delete_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=signal_controller.delete_asset, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/create-asset', methods=['POST'])
def create_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=signal_controller.add_asset, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/update-asset', methods=['POST'])
def update_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=signal_controller.update_asset, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})
# endregion

# todo crud strategy / add relation
# todo smt pair add
# todo close trade amend trade
# todo dashboard trade
# todo strategy testing

# region GET APP Route
@app.route('/get-trades', methods=['GET'])
def get_trades():
    return jsonify(signal_controller.get_trades())

@app.route('/get-assets', methods=['GET'])
def get_assets():
    return jsonify(signal_controller.get_assets())

@app.route('/get-strategies', methods=['GET'])
def get_strategies():
    return jsonify(signal_controller.get_strategies())
# endregion

# region Loging
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
# endregion
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
