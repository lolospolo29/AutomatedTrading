import datetime
from typing import Any

import pytz

from Models.DB.MongoDB import MongoDB
from Services.Helper.Mapper.Mapper import Mapper
from Services.Helper.SecretsManager import SecretsManager

ny_tz = pytz.timezone('America/New_York')


class mongoDBData:
    def __init__(self, secretsManager: SecretsManager, DataMapper: Mapper):
        self._SecretManager: SecretsManager = secretsManager
        self._DataMapper = DataMapper
        self._MongoDBData: MongoDB = MongoDB("TradingData", self._SecretManager.returnSecret("mongodb"))

    def addDataToDB(self, collectionName: str, data: Any) -> bool:
        self._MongoDBData.add(collectionName, data)
        return True

    def returnRetrieveOrDoArchive(self, asset: str, task: str) -> Any:
        currentTimeNy = datetime.datetime.now(ny_tz)

        # Berechne das Datum von vor 60 Tagen in der New Yorker Zeitzone
        date60DaysAgoNy = currentTimeNy - datetime.timedelta(days=60)

        # Umwandlung beider Zeiten in UTC
        currentTimeUtc = currentTimeNy.astimezone(pytz.utc)
        date60DaysAgoUtc = date60DaysAgoNy.astimezone(pytz.utc)

        Query = 'AssetData.timeStamp'

        if task == "retrieve":
            return self._MongoDBData.getDataWithinDateRange(asset, Query,
                                                            date60DaysAgoUtc,
                                                            currentTimeUtc)
        if task == "archive":
            self._MongoDBData.deleteOldDocuments(asset, Query, date60DaysAgoUtc)
