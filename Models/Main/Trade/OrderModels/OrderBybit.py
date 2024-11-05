class OrderData:
    def __init__(self, symbol, side, orderType, qty, price, timeInForce, stopLoss, takeProfit):
        self.symbol = symbol
        self.side = side
        self.orderType = orderType
        self.qty = qty
        self.price = price
        self.timeInForce = timeInForce
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
