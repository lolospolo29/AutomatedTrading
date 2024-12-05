import hashlib
import hmac
import time
from dataclasses import fields, is_dataclass
from typing import Any, Dict

import requests

from Models.API.Brokers.Bybit.GET.Response.TickersLinearInverse import TickersLinearInverse

api_key='hDrBURkbD5u57sB3aQ'
secret_key='TEfdN38XDQZjSa6u8j7p1A8IgLFfXT2z0f1Y'
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-demo.bybit.com" # Testnet endpoint

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
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    print(response.text)
    print(response.headers)
    print(Info + " Elapsed Time : " + str(response.elapsed))
    print(response.status_code)
    return response.json()

def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

# Create Order
# endpoint="/v5/order/create"
# method="POST"
# orderLinkId=uuid.uuid4().hex
# params='{"category":"linear","symbol": "BTCUSDT","side": "Buy","positionIdx": 0,"orderType": "Limit","qty": "0.01","price": "95300","takeProfit": "95700","timeInForce": "GTC","orderLinkId": "' + orderLinkId + '"}'
# HTTP_Request(endpoint,method,params,"Create")
#
# #Get unfilled Orders
# endpoint="/v5/order/realtime"
# method="GET"
# params='category=linear&settleCoin=USDT'
# HTTP_Request(endpoint,method,params,"UnFilled")

# #Cancel Order
# endpoint="/v5/order/cancel"
# method="POST"
# params='{"category":"linear","symbol": "BTCUSDT","orderLinkId": "'+orderLinkId+'"}'
# HTTP_Request(endpoint,method,params,"Cancel")

# Cancel All Orders
# endpoint="/v5/order/cancel-all"
# method="POST"
# params='{"category":"linear"}'
# HTTP_Request(endpoint,method,params,"Cancel")

# Get Position
# endpoint="/v5/position/list"
# method="GET"
# params='category=linear&symbol=BTCUSDT'
# HTTP_Request(endpoint,method,params,"Balance")


def from_dict(dataclass_type: Any, data: Dict[str, Any]) -> Any:
    """
    Convert a dictionary into a dataclass instance of type `dataclass_type`.
    """
    # Check if the dataclass_type is actually a dataclass
    if not is_dataclass(dataclass_type):
        raise TypeError(f"{dataclass_type} is not a dataclass")

    # Prepare the arguments for the dataclass constructor
    fieldnames = {field.name for field in fields(dataclass_type)}
    filtered_data = {key: value for key, value in data.items() if key in fieldnames}

    # For each field, if the field is a dataclass, recursively convert it
    for field in fields(dataclass_type):
        if is_dataclass(field.type) and field.name in filtered_data:
            filtered_data[field.name] = from_dict(field.type, filtered_data[field.name])

    # Create and return the dataclass instance
    return dataclass_type(**filtered_data)

# Price Tickers
endpoint="/v5/market/tickers"
method="GET"
params='category=linear&symbol=BTCUSDT'
a = HTTP_Request(endpoint,method,params,"Balance")
example = from_dict(TickersLinearInverse, a.get('result'))
print(example)
