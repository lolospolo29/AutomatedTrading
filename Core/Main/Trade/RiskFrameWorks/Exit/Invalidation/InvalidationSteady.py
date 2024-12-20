from Core.Main.Asset.SubModels.Candle import Candle


class InvalidationSteady:
    @staticmethod
    def checkInvalidation(stopLoss: float, candle: Candle, tradeDirection: str) ->bool:
        if tradeDirection == 'Buy':
            if candle.low < stopLoss:
                return True
            return False
        if tradeDirection == 'Sell':
            if candle.high > stopLoss:
                return True
            return False
