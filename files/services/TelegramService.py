from logging import Logger

import requests


class TelegramService:
    def __init__(self, token, chat_id, logger: Logger):
        self.__token = token
        self.__chat_id = chat_id
        self._logger = logger

    def send(self, message):
        url = f"https://api.telegram.org/bot{self.__token}/sendMessage?chat_id={self.__chat_id}&text={message}"
        try:
            requests.get(url)
        except requests.exceptions.RequestException as e:
            self._logger.error(f"Error While Sending to Telegram: {e}")
