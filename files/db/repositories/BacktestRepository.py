from files.db.MongoDB import MongoDB
from files.models.asset.AssetClass import AssetClass
from files.models.asset.Candle import Candle
from files.models.backtest.Result import Result
from files.models.trade.Trade import Trade

class BacktestRepository:

    def __init__(self, db_name: str, uri: str):
        self._db = MongoDB(db_name=db_name, uri=uri)

    # region Candle

    def add_candle(self, candle: Candle):
        self._db.add("Testdata", candle.model_dump(exclude={"_id"}))

    def find_candles_by_asset(self, asset:str)->list[Candle]:
        query = self._db.build_query("asset", asset)

        candles_db:list = self._db.find(collection_name="Testdata", query=query)
        candles:list[Candle] = []
        for candle in candles_db:
            candles.append(Candle(**candle))
        return candles

    # endregion

    # region Result

    def add_result(self, result:Result):
        self._db.add("Results",result.model_dump(exclude={"_id"}))

    def find_results(self)->list[Result]:
        results_db:list = self._db.find("Results",None)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    def find_result_by_result_id(self,result_id:int)->list[Result]:
        query = self._db.build_query("resultId", result_id)

        results_db:list = self._db.find("Results",query)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    def find_result_by_strategy(self,strategy:str)->list[Result]:
        query = self._db.build_query("strategy", strategy)

        results_db:list = self._db.find("Results",query)

        results:list[Result] = []
        for result in results_db:
            results.append(Result(**result))
        return results

    # endregion

    # region Asset Class

    def find_asset_class_by_id(self, asset:str)->AssetClass:
        query = self._db.build_query("assetClassId", asset)

        return AssetClass(**self._db.find("AssetClasses", query)[0])

    # endregion

    # region Trade

    def add_trade_to_db(self, trade: Trade):
        self._db.add("Trades",trade.model_dump(exclude={"_id"}))

    def find_trades(self)->list[Trade]:
        trades_db:list =  self._db.find("OpenTrades", None)

        trades:list[Trade] = []

        for trade_db in trades_db:
            trade = Trade(**trade_db)
            trades.append(trade)
        return trades

    def find_trade_by_id(self,trade_id:str)->Trade:
        query = self._db.build_query("tradeId", trade_id)
        return Trade(**self._db.find("OpenTrades", query)[0])

    def update_trade(self, trade: Trade):
        dto = self.find_trade_by_id(trade.trade_id)

        trade.id = dto.trade_id

        self._db.update("OpenTrades", trade.id, trade.model_dump(exclude={"strategy_id"}))

    # endregion

    def get_asset_selection(self):
        pipeline = [
            {"$group": {"_id": "$asset"}},  # Group by asset name
            {"$project": {"_id": 0, "asset": "$_id"}}  # Rename _id to asset
        ]

        return self._db.aggregate("Testdata", pipeline)