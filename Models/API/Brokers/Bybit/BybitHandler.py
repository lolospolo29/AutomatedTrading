from Models.API.Brokers.Bybit.GET.OpenAndClosedOrders import OpenAndClosedOrders
from Models.API.Brokers.Bybit.GET.Response.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from Models.API.ResponseParams import ResponseParams
from Models.Main.Brokers.Crypto.Bybit import Bybit


class BybitHandler:
    def __init__(self, broker: Bybit):
        self.broker: Bybit = broker

    def returnOpenAndClosedOrder(self,**kwargs):
        """
        Erstellen Sie ein Objekt von OpenAndClosedOrders und rufen Sie die Broker-API auf.
        :param kwargs: Parameter für OpenAndClosedOrders
        :return: Ergebnis der Broker-Anfrage
        """

        openAndClosedOrders: OpenAndClosedOrders = OpenAndClosedOrders(**kwargs)

        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The 'category' field is required.")

        param = openAndClosedOrders.toQueryString()

        endPoint = "/v5/order/realtime"
        method = "GET"

        responseJson = self.broker.sendRequest(endPoint, method, param)
        params = ResponseParams()
        result = params.fromDict(responseJson['result'], OpenAndClosedOrdersAll)

        return result


handler = BybitHandler(broker=Bybit("Bybit"))

# Aufruf mit nur einigen Parametern
response = handler.returnOpenAndClosedOrder(category="linear", settleCoin="USDT")
