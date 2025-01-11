from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.SMTPair import SMTPair


class Asset:

    # region Initializing
    def __init__(self, name: str,assetClass:str):
        self.name: str = name
        self.assetClass = assetClass
        self.brokers: list[str] = []
        self.strategies: list[str] = []
        self.smtPairs: list[SMTPair] = []
        self.CandlesSeries: list[CandleSeries] = []
        self.brokerStrategyAssignment: list[AssetBrokerStrategyRelation] = []
    # endregion

    # region Add Functions
    def addBroker(self, broker: str) -> bool:
        if not self._isBrokerInBrokers(broker):
            self.brokers.append(broker)
            return True
        return False

    def addStrategy(self, strategy: str) -> bool:
        if not self._isStrategyInStrategies(strategy):
            self.strategies.append(strategy)
            return True
        return False

    def addSMTPair(self, pair: SMTPair) -> bool:
        if not self._isPairInSMTPairs(pair):
            self.smtPairs.append(pair)
            return True
        return False

    def addCandleSeries(self, timeFrame: int, maxlen: int, broker: str) -> bool:
        for candleSeries in self.CandlesSeries:
            if not self._isBrokerAndTimeFrameInCandleSeries(broker, timeFrame, candleSeries):
                self.CandlesSeries.append(CandleSeries(timeFrame, maxlen, broker))
                return True
        if len(self.CandlesSeries) == 0:
            if self._isBrokerInBrokers(broker):
                self.CandlesSeries.append(CandleSeries(timeFrame, maxlen, broker))
                return True
            return False

    def addRelation(self, relation:AssetBrokerStrategyRelation) -> bool:
            if not self._isBrokerAndStrategyInAssignment(relation.broker, relation.strategy):
                if self._isBrokerInBrokers(relation.broker) and self._isStrategyInStrategies(relation.strategy):
                    self.brokerStrategyAssignment.append(relation)
                    return True
            return False

    def addCandle(self, candle: Candle) -> bool:
        for candleSeries in self.CandlesSeries:
            if self._isBrokerAndTimeFrameInCandleSeries(candle.broker, candle.timeFrame, candleSeries):
                candleSeries.addCandle(candle)
                return True
        raise ValueError("Candle is not in CandleSeries")
    # endregion

    # region Return Functions
    def returnCandles(self, timeFrame: int,broker: str) -> list[Candle]:
        for series in self.CandlesSeries:
            if self._isBrokerAndTimeFrameInCandleSeries(broker, timeFrame, series):
                return series.toList()
        return []

    def returnAllCandleSeries(self) -> list[CandleSeries]:
        allSeries = []
        for series in self.CandlesSeries:
            allSeries.append(series)
        return allSeries

    def returnSMTPair(self, pairName: str)-> SMTPair:
        for smtPair in self.smtPairs:
            for pair in smtPair.smtPairs:
                if pair == pairName:
                    return smtPair

    def returnRelationsForBroker(self, broker: str) -> list[AssetBrokerStrategyRelation]:
        relations: list[AssetBrokerStrategyRelation] = []
        for assignment in self.brokerStrategyAssignment:
            if broker == assignment.broker:
                relations.append(assignment)
        return relations
    # endregion

    # region Checkings
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
                    sorted(existingPair.smtPairs) == sorted(
                        pair.smtPairs)):  # Ensure elements match, regardless of order
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
    # endregion


