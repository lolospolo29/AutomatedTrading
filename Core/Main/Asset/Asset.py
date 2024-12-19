from Core.Main.Asset.SubModels.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Core.Main.Asset.SubModels.Candle import Candle
from Core.Main.Asset.SubModels.CandleSeries import CandleSeries
from Core.Main.Asset.SubModels.SMTPair import SMTPair


class Asset:
    def __init__(self, name: str):
        self.name: str = name
        self.brokers: list[str] = []
        self.strategies: list[str] = []
        self.smtPairs: list[SMTPair] = []
        self.CandlesSeries: list[CandleSeries] = []
        self.brokerStrategyAssignment: list[AssetBrokerStrategyRelation] = []

    def addBroker(self, broker: str) -> None:
        if not self._isBrokerInBrokers(broker):
            self.brokers.append(broker)

    def addStrategy(self, strategy: str) -> None:
        if not self._isStrategyInStrategies(strategy):
            self.strategies.append(strategy)

    def addSMTPair(self, pair: SMTPair) -> None:
        if not self._isPairInSMTPairs(pair):
            self.smtPairs.append(pair)

    def addCandleSeries(self, timeFrame: int, maxlen: int, broker: str) -> None:
        for candleSeries in self.CandlesSeries:
            if not self._isBrokerAndTimeFrameInCandleSeries(broker, timeFrame, candleSeries):
                self.CandlesSeries.append(CandleSeries(timeFrame, maxlen, broker))
                return
        if len(self.CandlesSeries) == 0:
            if self._isBrokerInBrokers(broker):
                self.CandlesSeries.append(CandleSeries(timeFrame, maxlen, broker))

    def addBrokerStrategyAssignment(self, broker: str, strategy: str) -> None:
            if not self._isBrokerAndStrategyInAssignment(broker, strategy):
                if self._isBrokerInBrokers(broker) and self._isStrategyInStrategies(strategy):
                    self.brokerStrategyAssignment.append(AssetBrokerStrategyRelation(self.name, broker, strategy))

    def addCandle(self, candle: Candle) -> None:
        for candleSeries in self.CandlesSeries:
            if self._isBrokerAndTimeFrameInCandleSeries(candle.broker, candle.timeFrame, candleSeries):
                candleSeries.addCandle(candle)
                return

    def returnCandles(self, timeFrame: int,broker: str) -> list:
        for candleSeries in self.CandlesSeries:
            if self._isBrokerAndTimeFrameInCandleSeries(broker, timeFrame, candleSeries):
                return candleSeries.toList()
        return []

    def returnAllCandleSeries(self):
        candleSeries = []
        for candleSerie in self.CandlesSeries:
            candleSeries.append(candleSerie)
        return candleSeries

    def returnBrokers(self,strategy: str) -> list:
        brokers = []
        for relation in self.brokerStrategyAssignment:
            if relation.strategy == strategy:
                brokers.append(relation.broker)
        return brokers

    def returnSMTPair(self, pairName: str):
        for smtPair in self.smtPairs:
            for pair in smtPair.smtPair:
                if pair == pairName:
                    return smtPair

    def returnRelationsForBroker(self, broker: str) -> list[AssetBrokerStrategyRelation]:
        strategies: list = []
        for assignment in self.brokerStrategyAssignment:
            if broker == assignment.broker:
                strategies.append(assignment)
        return strategies

    def _isBrokerInBrokers(self, broker: str) -> bool:
        if broker in self.brokers:
            return True
        return False

    def _isStrategyInStrategies(self, strategy: str) -> bool:
        if strategy in self.strategies:
            return True
        return False

    def _isPairInSMTPairs(self, pair: SMTPair) -> bool:
        for existingPair in self.smtPairs:
            if (existingPair.strategy == pair.strategy and
                    existingPair.correlation == pair.correlation and
                    sorted(existingPair.smtPair) == sorted(
                        pair.smtPair)):  # Ensure elements match, regardless of order
                print("Duplicate SMTPair found. Not adding to smtPairs.")
                return True
        return False

    @staticmethod
    def _isBrokerAndTimeFrameInCandleSeries(broker: str, timeFrame: int, candleSeries: CandleSeries)-> bool:
        if candleSeries.broker == broker and candleSeries.timeFrame == timeFrame:
            return True
        return False

    def _isBrokerAndStrategyInAssignment(self, broker: str, strategy: str) -> bool:
        for assignement in self.brokerStrategyAssignment:
            if assignement.strategy == strategy and assignement.broker == broker:
                return True
        return False


