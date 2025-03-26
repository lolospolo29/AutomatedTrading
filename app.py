import queue
import time
from threading import Thread

from flask import Flask, request, Response, render_template, jsonify

from files.ClassInstances import service_controller, logger, log_queue, asset_controller, \
    strategy_controller, relation_controller, smt_controller

app = Flask(__name__)


# region Asset

@app.route('/create-asset', methods=['POST'])
def create_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=asset_controller.create_asset, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/get-assets', methods=['GET'])
def get_assets():
    return jsonify(asset_controller.get_assets())

@app.route('/get-asset-classes', methods=['GET'])
def get_asset_classes():
    return jsonify(asset_controller.get_asset_classes())

@app.route('/update-asset', methods=['POST'])
def update_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=asset_controller.update_strategy, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/delete-asset', methods=['POST'])
def delete_asset():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=asset_controller.delete_strategy, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

# endregion

# region Relation

@app.route('/create-relation', methods=['POST'])
def create_relation():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=relation_controller.create_relation, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/get-relations', methods=['GET'])
def get_relations():
    return jsonify(relation_controller.get_relations())

@app.route('/get-categories', methods=['GET'])
def get_categories():
    return jsonify(relation_controller.get_categories())

@app.route('/update-relation', methods=['POST'])
def update_relation():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=relation_controller.update_relation, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/delete-relation', methods=['POST'])
def delete_relation():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=relation_controller.delete_relation, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

# endregion

# region Services

@app.route('/get-brokers', methods=['GET'])
def get_brokers():
    return jsonify(service_controller.get_brokers())

@app.route('/get-trades', methods=['GET'])
def get_trades():
    return jsonify(service_controller.get_trades())

@app.route('/get-news', methods=['GET'])
def get_news():
    return jsonify(service_controller.get_news())

@app.route('/get-asset-selection', methods=['GET'])
def get_asset_selection():
    return jsonify(service_controller.get_asset_selection())

@app.route('/get-test-results', methods=['POST'])
def get_test_results():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")  #
    result = service_controller.get_test_results(json_data)

    return jsonify(result)

@app.route('/run-backtest', methods=['POST'])
def run_backtest():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=service_controller.run_backtest, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/tradingview', methods=['post'])
def receive_signal():
    json_data = request.get_json()

    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=service_controller.trading_view_signal, args=(json_data,))
    thread.start()

    return f'Received Analyse data: {json_data}'

@app.route('/atr', methods=['post'])
def receive_atr():
    json_data = request.get_json()

    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=service_controller.atr_signal, args=(json_data,))
    thread.start()

    return f'Received Analyse data: {json_data}'

# endregion

# region SMT Pair

@app.route('/create-smt-pair', methods=['POST'])
def create_smt_pair():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=smt_controller.create_smt_pair, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/get-smt-pairs', methods=['GET'])
def get_smt_pairs():
    return jsonify(smt_controller.get_smt_pairs())

@app.route('/delete-smt-pair', methods=['POST'])
def delete_smt_pair():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=smt_controller.delete_smt_pair, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

# endregion

# region Strategy

@app.route('/create-strategy', methods=['POST'])
def create_strategy():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=strategy_controller.create_strategy, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/get-strategies', methods=['GET'])
def get_strategies():
    return jsonify(strategy_controller.get_strategies())

@app.route('/get-entry-exit-strategies', methods=['GET'])
def get_entry_exit_strategies():
    return jsonify(strategy_controller.get_entry_exit_strategies())

@app.route('/update-strategy', methods=['POST'])
def update_strategy():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=strategy_controller.update_strategy, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

@app.route('/delete-strategy', methods=['POST'])
def delete_relation():
    json_data = request.get_json()  # Get the JSON data sent with the POST request
    logger.debug(f"Received signal data: {json_data}")

    thread = Thread(target=strategy_controller.delete_strategy, args=(json_data,))
    thread.start()

    return jsonify({"status": "success"})

# endregion

# endregion

# region Loging
@app.route('/')
def show_logs():
    return render_template('showLogs.html')


@app.route('/stream')
def stream_logs():
    def generate():
        timeout_limit = 3  # Close connection if no logs in 60 seconds
        start_time = time.time()

        while True:
            try:
                log_entry = log_queue.get(timeout=1)  # Wait max 5s
                yield f"data: {log_entry}\n\n"
                log_queue.task_done()
                start_time = time.time()  # Reset timeout timer
            except queue.Empty:
                if time.time() - start_time > timeout_limit:
                    yield "data: Stream closed due to inactivity\n\n"
                    break  # Exit loop if no logs for too long

    return Response(generate(), mimetype='text/event-stream')


# endregion

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
