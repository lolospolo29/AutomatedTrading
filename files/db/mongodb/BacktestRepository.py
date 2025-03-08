from files.db.mongodb.MongoDB import MongoDB
from files.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from files.db.mongodb.dtos.AssetDTO import AssetDTO
from files.db.mongodb.dtos.TradeDTO import TradeDTO
from files.mappers.DTOMapper import DTOMapper
from files.models.asset.Candle import Candle
from files.models.backtest.Result import Result
from files.models.trade.Trade import Trade


class BacktestRepository:
    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)
        self._dto_mapper = DTOMapper()

    def add_candle(self, candle: Candle):
        self._db.add("Testdata", candle.model_dump())

    def find_candles_by_asset(self, asset:str)->list[Candle]:
        query = self._db.buildQuery("asset", asset)

        candles_db:list = self._db.find(collectionName="Testdata",query=query)
        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles

    def find_asset_class_name_by_asset(self, asset:str)->str:
        query = self._db.buildQuery("name", asset)

        asset_dto:AssetDTO = AssetDTO(**self._db.find("Asset", query)[0])

        query = self._db.buildQuery("assetClassId", asset_dto.assetClass)

        return AssetClassDTO(**self._db.find("AssetClasses", query)[0]).name

    def find_assets_in_testdata(self)->list[str]:
        candles_db: list = self._db.find(collectionName="Testdata", query=None)

        # Nutze ein Set für eindeutige Assets
        assets = {Candle(**candle).asset for candle in candles_db}

        # Konvertiere das Set zurück in eine Liste
        return list(assets)

    def add_result(self,result:Result):
        self._db.add("Results",result.model_dump())

    def find_results(self)->list[Result]:
        results_db:list = self._db.find("Results",None)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    def find_result_by_result_id(self,result_id:int)->list[Result]:
        query = self._db.buildQuery("result_id", result_id)

        results_db:list = self._db.find("Results",query)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    def find_result_by_strategy(self,strategy:str)->list[Result]:
        query = self._db.buildQuery("strategy", strategy)

        results_db:list = self._db.find("Results",query)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    def find_trades(self)->list[TradeDTO]:
        trades_db:list =  self._db.find("OpenTrades", None)

        trades:list[TradeDTO] = []

        for trade_db in trades_db:
            trade = TradeDTO(**trade_db)
            trades.append(trade)
        return trades

    def find_trade_by_id(self,trade_id:str)->TradeDTO:
        query = self._db.buildQuery("tradeId", trade_id)
        return TradeDTO(**self._db.find("OpenTrades", query)[0])

    def add_trade_to_db(self, trade: Trade):

        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        self._db.add("OpenTrades",trade_dto.model_dump())

    def update_trade(self, trade: Trade):

        query = self._db.buildQuery( "tradeId", str(trade.id))
        res = self._db.find("OpenTrades", query)
        trade_dto:TradeDTO = self._dto_mapper.map_trade_to_dto(trade=trade)
        self._db.update("OpenTrades", res[0].get("_id"), trade_dto.model_dump())