from typing import Any

from Interfaces.Strategy.IConfirmation import IConfirmation
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Structure import Structure


class BOS(IConfirmation):
    def __init__(self, lookback: int):
        self.lookback: int = lookback

    def returnConfirmation(self, candles: list[Candle]) -> Any:
        """
        Identify Break of Structure (BOS) from provided data.
        param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'BOS_Bullish', 'BOS_Bearish' or None.
        """
        lookback = self.lookback
        highs = [data['high'] for data in candles]
        lows = [data['low'] for data in candles]
        closes = [data['close'] for data in candles]

        lastBullishHigh = None
        lastBearishLow = None

        for i in range(len(candles)):
            # Track the last significant bullish high
            if i >= lookback:
                if closes[i] > max(highs[i - lookback:i]):
                    lastBullishHigh = closes[i]
                return Structure(name="BOS", direction="Bullish")

            # Track the last significant bearish low
            if i >= lookback:
                if closes[i] < min(lows[i - lookback:i]):
                    lastBearishLow = closes[i]
                    return Structure(name="BOS", direction="Bearish")
