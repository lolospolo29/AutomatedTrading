from Core.Main.Asset.SubModels import Candle
from Core.Main.Strategy.FrameWorks.Structure import Structure
from Interfaces.Strategy.IConfirmation import IConfirmation


class BOS(IConfirmation):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "BOS"

    def returnConfirmation(self, candles: list[Candle]) -> list:
        """
        Identify Break of Structure (BOS) from provided data.
        param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'BOS_Bullish', 'BOS_Bearish' or None.
        """
        if len(candles) < self.lookback:
            return []
        highs = []
        lows = []
        closes = []
        ids = []
        structures = []

        for candle in candles:
            highs.append(candle.high)
            lows.append(candle.low)
            closes.append(candle.close)
            ids.append(candle.id)

        lastBullishHigh = None
        lastBullishHighId = None
        lastBearishLow = None
        lastBearishLowId = None

        for i in range(len(candles)):
            # Track the last significant bullish high
            if i >= self.lookback:
                if closes[i] > max(highs[i - self.lookback:i]):
                    lastBullishHigh = closes[i]
                    lastBullishHighId = ids[i]
                structure = Structure(self.name, direction="Bullish", id=lastBullishHighId)
                structures.append(structure)

            # Track the last significant bearish low
            if i >= self.lookback:
                if closes[i] < min(lows[i - self.lookback:i]):
                    lastBearishLow = closes[i]
                    lastBearishLowId = ids[i]
                    structure = Structure(self.name, direction="Bearish", id=lastBearishLowId)
                    structures.append(structure)

        return structures
