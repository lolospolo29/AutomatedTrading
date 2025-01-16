import hashlib
import hmac
import time

import requests as requests

from app.manager.initializer.SecretsManager import SecretsManager


class Bybit:

    def __init__(self,name: str):
        self.name = name
        self._SecretManager: SecretsManager = SecretsManager()
        self.apiKey: str = self._SecretManager.returnSecret("BybitKey")
        self.apiSecret: str = self._SecretManager.returnSecret("BybitSecret")
        self.baseUrl = self._SecretManager.returnSecret("BybitUrl")
        self.recvWindow = str(5000)
        self.session = requests.Session()

    def sendRequest(self,endPoint,method,payload) -> dict:
        timeStamp = str(int(time.time() * 10 ** 3))
        signature = self.genSignature(payload,timeStamp)
        headers = {
            'X-BAPI-API-KEY': self.apiKey,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timeStamp,
            'X-BAPI-RECV-WINDOW': self.recvWindow,
            'Content-Type': 'application/json'
        }

        if (method=="post"):
            response = self.session.request(method, self.baseUrl + endPoint, headers=headers, data=payload)
        else:
            response = self.session.request(method, self.baseUrl + endPoint + "?" + payload, headers=headers)
        return response.json()

    def genSignature(self,payload,timeStamp):
        param_str = str(timeStamp) + self.apiKey + self.recvWindow + payload

        hash = hmac.new(bytes(self.apiSecret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()

        return signature
bh = Bybit("BTC")