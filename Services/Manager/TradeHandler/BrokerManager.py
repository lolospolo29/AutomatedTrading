from Core.Main.Brokers.Broker import Broker


class BrokerManager:
    def __init__(self):
        self.brokers: dict = {}

    def registerBroker(self, broker: Broker):
        self.brokers[broker.name] = broker
        print(f"Broker '{broker.name}' created and added to the Broker Manager.")
