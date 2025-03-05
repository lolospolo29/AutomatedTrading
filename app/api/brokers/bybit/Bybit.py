import hashlib
import hmac
import time

import requests as requests

from app.helper.manager.initializer.SecretsManager import SecretsManager


class Bybit:

    def __init__(self,name: str):
        self.name = name
        self._secret_manager: SecretsManager = SecretsManager()
        self.__apiKey: str = self._secret_manager.return_secret("BybitKey")
        self.__apiSecret: str = self._secret_manager.return_secret("BybitSecret")
        self.__baseUrl = self._secret_manager.return_secret("BybitUrl")
        self.__recvWindow = str(5000)
        self.__session = requests.Session()

    def send_request(self, end_point, method, payload) -> dict:
        timeStamp = str(int(time.time() * 10 ** 3))
        signature = self.gen_signature(payload, timeStamp)
        headers = {
            'X-BAPI-API-KEY': self.__apiKey,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timeStamp,
            'X-BAPI-RECV-WINDOW': self.__recvWindow,
            'Content-Type': 'application/json'
        }

        if method == "post":
            response = self.__session.request(method, self.__baseUrl + end_point, headers=headers, data=payload)
        else:
            response = self.__session.request(method, self.__baseUrl + end_point + "?" + payload, headers=headers)
        return response.json()

    def gen_signature(self, payload, time_stamp):
        param_str = str(time_stamp) + self.__apiKey + self.__recvWindow + payload

        hash = hmac.new(bytes(self.__apiSecret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()

        return signature
