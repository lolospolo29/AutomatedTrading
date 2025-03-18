import logging

import requests
import urllib.parse


class TelegramLogHandler(logging.Handler):
    def __init__(self,token,chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        log_entry = urllib.parse.quote(log_entry)  # Korrektur: URL-Encode für Sonderzeichen
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={log_entry}"
        try:
            requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Senden an Telegram: {e}")