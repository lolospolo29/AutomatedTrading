import time
from functools import partial
from threading import Thread

from watchdog.observers import Observer

from app.controller.SignalController import SignalController
from tools.FileHandler import FileHandler
from app.manager.initializer.ConfigManager import ConfigManager

configManager = ConfigManager()

# FileHandler
newFileHandler = FileHandler()

# controller

signalController = SignalController()

# Logic

configManager.runStartingSetup()


def monitorFolder(handler, folderPath):
    observer = Observer()
    observer.schedule(handler, path=folderPath, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keeps the script running

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

thread = Thread(target=partial(monitorFolder, newFileHandler, "/Users/lauris/PycharmProjects/AutomatedTrading/incomingFiles"))
thread.start()
