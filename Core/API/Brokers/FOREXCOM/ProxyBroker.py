from Core.API.Brokers.Broker import Broker


class ProxyBroker(Broker):
    def genSignature(self, payload):
        pass

    def sendRequest(self, endPoint, method, payload):
        pass
