import hashlib
import hmac
import time

import requests as requests

from Models.Main.Brokers.Broker import Broker


class Bybit(Broker):

    def __init__(self,name: str):
        super().__init__(name)
        self.apiKey: str = ''
        self.apiSecret: str = ''
        self.baseUrl: str = 'https://api.bybit.com'

    def generateSignature(self, params):
        """Generate HMAC SHA256 signature."""
        sorted_params = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        return hmac.new(self.apiSecret.encode(), sorted_params.encode(), hashlib.sha256).hexdigest()

    def trailStop(self):
        pass

    def cancelOrder(self):
        pass

    def getOrderInformation(self):
        pass

    def executeMarketOrder(self, order):
        """Place a trading order with stop loss and take profit on Bybit."""
        endpoint = '/v5/order/create'
        url = self.baseUrl + endpoint

        params = {
            'api_key': self.apiKey,
            'symbol': order.symbol,
            'side': order.side,
            'order_type': order.orderType,
            'qty': order.qty,
            'price': order.price,
            'time_in_force': order.timeInForce,
            'stop_loss': order.stopLoss,
            'take_profit': order.takeProfit,
            'timestamp': str(int(time.time() * 1000))
        }

        # Remove None values
        params = {key: value for key, value in params.items() if value is not None}

        params['sign'] = self.generateSignature(params)
        response = requests.post(url, data=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Request failed', 'status_code': response.status_code}

    def setLimitOrder(self):
        pass

    def getBalance(self):
        pass
