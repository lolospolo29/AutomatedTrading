from Models.Asset import SMTPair, CandleSeries


class Asset:
    def __init__(self, name: str, strategies: list[str], smtPairs: list[str], brokers: list):
        self.name: str = name
        self.strategies: list[str] = strategies
        self.brokers: list[str] = brokers
        self.smtPairs: list[SMTPair] = smtPairs
        self.CandlesSeries: list[CandleSeries] = []
        self.brokerStrategyAssignment: dict = {}

    def addCurrentData(self, tradingData):
        for assetData in self.currentData:
            if assetData.timeFrame == tradingData.timeFrame:
                assetData.addData(tradingData.open, tradingData.high, tradingData.low, tradingData.close,
                                  tradingData.time)
                break

    def returnCurrentDataByIds(self, _ids):
        collectedIdData = []
        for assetData in self.currentData:
            collectedIdData.append(assetData.getDataByIds(_ids))
        return collectedIdData

    def returnAllTimeFrames(self):
        """Gibt eine Liste aller timeFrames zurück, die in dataStorage gespeichert sind."""
        return [assetData.timeFrame for assetData in self.currentData]

    def returnCurrentDataByTimeFrameAndDataPoints(self, timeframe, numberOfDataPoints):
        """
        Fetch the last 'number_of_data_points' for the given timeframe.
        This is useful for retrieving historical data for analysis.
        """
        for assetData in self.currentData:
            if assetData.timeFrame == timeframe:
                # Ensure we don't request more data than we have
                availableDataPoints = min(len(assetData.open), numberOfDataPoints)

                historical_data = {
                    'open': list(assetData.open)[-availableDataPoints:],
                    'high': list(assetData.high)[-availableDataPoints:],
                    'low': list(assetData.low)[-availableDataPoints:],
                    'close': list(assetData.close)[-availableDataPoints:],
                    'time': list(assetData.time)[-availableDataPoints:]
                }
                return historical_data
