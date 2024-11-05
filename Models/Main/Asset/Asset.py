from Models.Main.Asset.BrokerStrategyAssignment import BrokerStrategyAssignment
from Models.Main.Asset.Candle import Candle
from Models.Main.Asset.CandleSeries import CandleSeries
from Models.Main.Asset.SMTPair import SMTPair


class Asset:
    def __init__(self, name: str):
        self.name: str = name
        self.strategies: list[str] = []
        self.brokers: list[str] = []
        self.smtPairs: list[SMTPair] = []
        self.CandlesSeries: list[CandleSeries] = []
        self.brokerStrategyAssignment: list[BrokerStrategyAssignment] = []

    def addStrategy(self, strategy: str) -> None:
        if not self.isStrategyInStrategies(strategy):
            self.strategies.append(strategy)

    def addBroker(self, broker: str) -> None:
        if not self.isBrokerInBrokers(broker):
            self.brokers.append(broker)

    def addSMTPair(self, pair: SMTPair) -> None:
        if not self.isPairInSMTPairs(pair):
            self.smtPairs.append(pair)

    def addCandleSeries(self, timeFrame: int, maxlen: int, broker: str) -> None:
        for candleSeries in self.CandlesSeries:
            if not self.isBrokerAndTimeFrameInCandleSeries(broker, timeFrame,candleSeries):
                break
        self.CandlesSeries.append(CandleSeries(timeFrame, maxlen, broker))

    def addCandle(self, candle: Candle) -> None:
        for candleSeries in self.CandlesSeries:
            if not self.isBrokerAndTimeFrameInCandleSeries(candle.broker, candle.timeFrame,candleSeries):
                candleSeries.addCandle(candle)
                break

    def brokerStrategyAssignment(self, broker: str, strategy: str) -> None:
            if not self.isBrokerAndStrategyInAssignment(broker, strategy):
                self.brokerStrategyAssignment.append(BrokerStrategyAssignment(broker, strategy))

    def isStrategyInStrategies(self, strategy: str) -> bool:
        if strategy in self.strategies:
            return True
        return False

    def isBrokerInBrokers(self, broker: str) -> bool:
        if broker in self.brokers:
            return True
        return False

    def isPairInSMTPairs(self, pair: SMTPair) -> bool:
        for existingPair in self.smtPairs:
            if (existingPair.strategy == pair.strategy and
                    existingPair.correlation == pair.correlation and
                    sorted(existingPair.smtPair) == sorted(
                        pair.smtPair)):  # Ensure elements match, regardless of order
                print("Duplicate SMTPair found. Not adding to smtPairs.")
                return True
        return True
    @staticmethod
    def isBrokerAndTimeFrameInCandleSeries(broker: str, timeFrame: int, candleSeries: CandleSeries)-> bool:
        if candleSeries.broker == broker and candleSeries.timeFrame == timeFrame:
            return True
        return False

    def isBrokerAndStrategyInAssignment(self, broker: str, strategy: str) -> bool:
        for assignement in self.brokerStrategyAssignment:
            if assignement.strategy == strategy and assignement.broker == broker:
                return True
        return False


