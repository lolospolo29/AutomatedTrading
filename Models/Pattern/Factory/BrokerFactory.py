from Interfaces.IFactory import IFactory
from Models.Main.Brokers.Broker import Broker
from Models.Main.Brokers.Crypto.Bybit import Bybit
from Models.Main.Brokers.Forex.ProxyBroker import ProxyBroker


class BrokerFactory(IFactory):
    def returnClass(self, name: str) -> Broker:
        if name == "BYBIT":
            return Bybit(name)
        if name == "CAPITALCOM":
            return ProxyBroker(name)