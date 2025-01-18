import time
from functools import partial
from threading import Thread

from watchdog.observers import Observer

from app.controller.SignalController import SignalController
from tools.FileHandler import FileHandler
from app.manager.initializer.ConfigManager import ConfigManager

config_manager = ConfigManager()

# FileHandler
new_file_handler = FileHandler()

# controller

signal_controller = SignalController()

# Logic

config_manager.run_starting_setup()


def MonitorFolder(handler, folderPath):
    observer = Observer()
    observer.schedule(handler, path=folderPath, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keeps the script running

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

thread = Thread(target=partial(MonitorFolder, new_file_handler, "/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles"))
thread.start()
