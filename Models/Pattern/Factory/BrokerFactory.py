from Interfaces.IFactory import IFactory
from Models.Main.Brokers.Broker import Broker
from Models.Main.Brokers.Bybit import Bybit


class BrokerFactory(IFactory):
    def returnClass(self, name: str) -> Broker:
        if name == "BYBIT":
            return Bybit(name)