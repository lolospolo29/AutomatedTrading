from typing import Any

from Models.DB.MongoDB import MongoDB
from Models.Main.Trade import Trade
from Services.Helper.Mapper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager


class mongoDBTrades:
    def __init__(self, secretsManager: SecretsManager, DataMapper: Mapper):
        self._SecretManager: SecretsManager = secretsManager
        self._DataMapper: Mapper = DataMapper
        self._MongoDBTrades: MongoDB = MongoDB("Trades", self._SecretManager.returnSecret("mongodb"))

    def addTradeToDB(self, trade: Any) -> bool:
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
