from Models.Main.Brokers.Broker import Broker


class BrokerManager:
    def __init__(self):
        self.brokers: dict = {}

    def registerBroker(self, broker: Broker):
        self.brokers[broker.name] = broker
        print(f"Asset '{broker.name}' created and added to the controller.")
