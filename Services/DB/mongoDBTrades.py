from Models.DB.MongoDB import MongoDB
from Models.Trade import Trade


class mongoDBTrades:
    def __init__(self, secretsManager, DataMapper):
        self._secretManager = secretsManager
        self._DataMapper = DataMapper
        self._MongoDBTrades = MongoDB("Trades", secretsManager.returnSecret("mongodb"))

    def addTradeToDB(self, trade: Trade) -> bool:
        self._MongoDBTrades.add("OpenTrades", trade)
        return True

    def archiveCloseTrade(self, closedTradeList: list[Trade]) -> bool:
        query = self._MongoDBTrades.buildQuery("Trade", "status", "closed")
        self._MongoDBTrades.deleteByQuery("OpenTrades", query)
        self._MongoDBTrades.add("ClosedTrades", closedTradeList)
        return True

    def returnOpenTrades(self) -> list:
        tradeList = self._MongoDBTrades.find("OpenTrades", None)
        openTrades = []
        if not len(tradeList) < 0:
            for trade in tradeList:
                openTrades.append(self._DataMapper.MapToClass(trade))
        return openTrades
