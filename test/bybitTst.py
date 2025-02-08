import hashlib
import hmac
import json
import time

import requests as requests

from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.manager.initializer.SecretsManager import SecretsManager

sm: SecretsManager = SecretsManager()

api_key= sm.return_secret("demoBybitAPiKey")
secret_key= sm.return_secret("demoBybitAPiSecret")
httpClient=requests.Session()
recv_window=str(5000)
url= sm.return_secret("demoBybitUrl") # Testnet endpoint


# noinspection PyShadowingNames,PyUnusedLocal
def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }

    # noinspection PyRedundantParentheses
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    return response.json()


# noinspection PyShadowingNames
def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload

    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()

    return signature

#Create Order
endpoint="/v5/order/create"
method="POST"
create = PlaceOrder(category="linear", symbol="ETHUSDT", side="Buy", orderType="Limit", qty="0.3",price="3000")
params = create.to_dict()
createRes = HTTP_Request(endpoint, method, params, "Create")
orderId = createRes["result"]["orderId"]
time.sleep(2)

# Create Order
# endpoint="/v5/order/amend"
# method="POST"
# amend = AmendOrder(category="linear", symbol="ETHUSDT",orderId=orderId,tpTriggerBy="MarkPrice",takeProfit="4000")
# params = amend.to_dict()
# amendRes = HTTP_Request(endpoint, method, params, "Create")
# time.sleep(2)

#Get unfilled Orders
# endpoint = "/v5/order/realtime"
# method = "GET"
# params = 'category=linear&settleCoin=BTCUSDT'
# HTTP_Request(endpoint,method,params,"UnFilled")
# time.sleep(2)

# Cancel Order
# endpoint="/v5/order/cancel"
# method="POST"
# params='{"category":"linear","symbol": "BTCUSDT","orderLinkId": "'+orderId+'"}'
# HTTP_Request(endpoint,method,params,"Cancel")
# time.sleep(2)

#Cancel All Orders
# endpoint="/v5/order/cancel-all"
# method="POST"
# order = CancelAllOrders(category="linear",symbol="ETHUSDT")
# params = order.to_dict()
# HTTP_Request(endpoint,method,params,"Cancel")
# time.sleep(2)

# Get Position
# endpoint="/v5/position/list"
# method="GET"
# params='category=linear&symbol=BTCUSDT'
# HTTP_Request(endpoint,method,params,"Balance")


# # Price Tickers
# endpoint="/v5/market/tickers"
# method="GET"
# tickers = Tickers(category="linear",symbol="BTCUSDT")
# tickersParam = tickers.to_query_string()
# a = HTTP_Request(endpoint,method,tickersParam,"Balance")

# Add Margin
# endpoint="/v5/market/add-margin"
# method="POST"
# tickers = AddOrReduceMargin(category="linear",symbol="ETHUSDT",margin="0.33")
# tickersParam = tickers.to_dict()
# a = HTTP_Request(endpoint,method,tickersParam,"Balance")

# Batch Place Order
endpoint="/v5/order/create-batch"
method="POST"
payload = {
  "category": "linear",
  "request": [
    {
      "symbol": "BTCUSDT",
      "side": "Buy",
      "orderType": "Limit",
      "isLeverage": 0,
      "qty": "0.05",
      "price": "30000",
      "timeInForce": "GTC",
      "orderLinkId": "spot-btc-03"
    },
    {
      "symbol": "ATOMUSDT",
      "side": "Sell",
      "orderType": "Limit",
      "isLeverage": 0,
      "qty": "2",
      "price": "12",
      "timeInForce": "GTC",
      "orderLinkId": "spot-atom-03"
    }
  ]
}
a = HTTP_Request(endpoint,method,json.dumps(payload),"Balance")
b = a

