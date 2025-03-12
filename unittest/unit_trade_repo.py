# mongo_trades = MongoDBTrades()
#
# trade = Trade(relation=Relation(asset="BTC",broker="bc",strategy="a",id=1,max_trades=1),id="31")
#
# mongo_trades.add_trade_to_db(trade)
#
# trades = mongo_trades.find_trades()
#
# candle = Candle(asset="BTC",broker="bc",open=234,high=131,low=123,close=22,iso_time=datetime.now(),timeframe=1)
#
# pd = PDArray(candles=[candle])
# pd.name = "test"
# pd.orderLinkId = "131"
#
# mongo_trades.add_framework_to_db(pd)
#
# frameworks_db = mongo_trades.find_frameworks_by_orderLinkId(pd.orderLinkId)
#
# pd.status = "a"
#
# mongo_trades.update_framework(pd)
#
# mongo_trades.add_framework_candles_to_db(pd)