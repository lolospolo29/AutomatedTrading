from Core.Main.Asset.SubModels.Candle import Candle


class CE:
    @staticmethod
    def getEntry(candle: Candle):
        return (candle.open + candle.close) * 0,5
