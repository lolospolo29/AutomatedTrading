from threading import Thread

from flask import Flask, request

from Initializing.ClassInstances import signalController

app = Flask(__name__)


@app.route('/tradingview', methods=['POST'])
def receive_signal():
    jsonData = request.get_json()

    thread = Thread(target=signalController.tradingViewSignal(jsonData))
    thread.start()

    return f'Received Analyse data: {jsonData}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# API Secrets
# Name : DemoApiKey
# Api Key : Ifp91Iy8fOY6x22bVG
# Secret: eagubhmZG5nY0gbycEeJNGR50GuT5YnpZA37
