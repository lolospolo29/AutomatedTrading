import hashlib
import hmac
import time
from typing import Union

import requests as requests

from Models.API.GETParams import GETParams
from Models.API.POSTParams import POSTParams
from Models.Main.Brokers.Broker import Broker


class Bybit(Broker):

    def __init__(self,name: str):
        super().__init__(name)
        self.apiKey: str = 'hDrBURkbD5u57sB3aQ'
        self.apiSecret: str = 'TEfdN38XDQZjSa6u8j7p1A8IgLFfXT2z0f1Y'
        self.baseUrl: str = 'https://api-demo.bybit.com'
        self.recvWindow = str(5000)
        self.timeStamp = None

    def sendRequest(self,endPoint,method,payload) -> dict:
        httpClient = requests.Session()
        self.timeStamp = str(int(time.time() * 10 ** 3))
        signature = self.genSignature(payload)
        headers = {
            'X-BAPI-API-KEY': self.apiKey,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': self.timeStamp,
            'X-BAPI-RECV-WINDOW': self.recvWindow,
            'Content-Type': 'application/json'
        }
        if method == "POST":
            response = httpClient.request(method, self.baseUrl + endPoint, headers=headers, data=payload)
        else:
            response = httpClient.request(method, self.baseUrl + endPoint + "?" + payload, headers=headers)

        return response.json()

    def genSignature(self,payload):
        param_str = str(self.timeStamp) + self.apiKey + self.recvWindow + payload
        hash = hmac.new(bytes(self.apiKey, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def prepareAndSendRequest(self, params: Union[POSTParams, GETParams], endPoint, method) -> dict:
        param = None

        if isinstance(params, POSTParams):
            param =  params.toDict()
        elif isinstance(params, GETParams):
            param = params.toQueryString()

        return self.sendRequest(endPoint, method, param)



bybit = Bybit("Bybit")
bybit.executeMarketOrder()
