from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure


class BOS(IConfirmation):

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "BOS"

    def return_confirmation(self, candles: list[Candle]) -> list[Structure]:
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
        structures = []

        for candle in candles:
            highs.append(candle.high)
            lows.append(candle.low)
            closes.append(candle.close)

        last_bullish_high_candle = None
        last_bearish_low_candle = None

        for i in range(len(candles)):
            # Track the last significant bullish high
            if i >= self.lookback:
                if closes[i] > max(highs[i - self.lookback:i]):
                    last_bullish_high_candle = candles[i]
                structure = Structure(self.name, direction="Bullish", candle=last_bullish_high_candle)
                structures.append(structure)

            # Track the last significant bearish low
            if i >= self.lookback:
                if closes[i] < min(lows[i - self.lookback:i]):
                    last_bearish_low_candle = candles[i]
                    structure = Structure(self.name, direction="Bearish",candle=last_bearish_low_candle)
                    structures.append(structure)

        return structures
