from Core.API.Brokers.Bybit.Bybit import Bybit
from Core.Main.Brokers.Broker import Broker
from Core.Main.Brokers.Forex.ProxyBroker import ProxyBroker
from Interfaces.IFactory import IFactory


class BrokerFactory(IFactory):
    def returnClass(self, name: str) -> Broker:
        if name == "BYBIT":
            return Bybit(name)
        if name == "CAPITALCOM":
            return ProxyBroker(name)