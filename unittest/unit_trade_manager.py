# trade_manager = TradeManager()
#
# relation = Relation(asset="XRPUSDT", broker="BYBIT", strategy="AC", max_trades=1, id=1)
# relation2 = Relation(asset="XRPUSDT", broker="BYBIT", strategy="ABC", max_trades=1, id=2)
#
# pd = PDArray(candles=[])
#
# order1 = Order(confirmations=[pd])
#
# order1.orderType = OrderTypeEnum.MARKET.value
# order1.order_result_status = OrderResultStatusEnum.NEW.value
# order1.category = "linear"
# order1.symbol = "XRPUSDT"
# order1.qty = str(3)
# order1.price = str(3.1)
# order1.orderLinkId = uuid.uuid4().__str__()
# order1.side = "Buy"
# order1.order_result_status = OrderResultStatusEnum.NEW.value
#
# order2 = Order()
#
# order2.orderType = OrderTypeEnum.LIMIT.value
# order2.category = "linear"
# order2.symbol = "XRPUSDT"
# order2.qty = str(3)
# order2.price = str(3.2)
# order2.triggerPrice = str(3.3)
# order2.triggerDirection = 1
# order2.orderLinkId = uuid.uuid4().__str__()
# order2.side = "Sell"
# order2.order_result_status = OrderResultStatusEnum.NEW.value
#
# trade1 = Trade(relation=relation, orders=[order1, order2], tradeId="131", category="linear")
#
# trade_manager.register_trade(trade1)
#
# print(trade_manager.return_trades_for_relation(relation))
#
# trades = trade_manager.return_trades_for_relation(relation2)
#
# trade_manager.place_trade(trade1)
#
# trades2 = trade_manager.return_trades_for_relation(relation)
#
# for res1 in trades2:
#     trade_manager.update_trade(res1)
#
# trades3 = trade_manager.return_trades_for_relation(relation)
#
# for res2 in trades3:
#     trade_manager.cancel_trade(res2)