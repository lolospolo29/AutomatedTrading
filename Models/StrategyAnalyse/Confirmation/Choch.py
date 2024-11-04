from Interfaces.Strategy.IConfirmation import IConfirmation
from Models.Asset import Candle
from Models.StrategyAnalyse.Structure import Structure


class Choch(IConfirmation):

    def __init__(self, lookback: int):
        self.lookback: int = lookback

    @staticmethod
    def isBullishFractal(highs: list, index: int, lookback: int) -> bool:
        """Check if there is a bullish fractal at the given index (local high)"""
        p = lookback // 2
        if index < p or index >= len(highs) - p:
            return False
        # Check if it's a local maximum
        for i in range(1, p + 1):
            if highs[index] <= highs[index - i] or highs[index] <= highs[index + i]:
                return False
        return True

    @staticmethod
    def isBearishFractal(lows: list, index: int, lookback: int) -> bool:
        """Check if there is a bearish fractal at the given index (local low)"""
        p = lookback // 2
        if index < p or index >= len(lows) - p:
            return False
        # Check if it's a local minimum
        for i in range(1, p + 1):
            if lows[index] >= lows[index - i] or lows[index] >= lows[index + i]:
                return False
        return True

    def getConfirmation(self, candles: list[Candle]) -> Structure:
        """
        Identify Change of Character (ChoCH) from provided data.
        _param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'Choch_Bullish', 'Choch_Bearish' or None.
        """
        lookback = self.lookback
        highs = [data['high'] for data in candles]
        lows = [data['low'] for data in candles]
        closes = [data['close'] for data in candles]

        upperFractal = None
        lowerFractal = None
        os = 0  # Keeps track of the order of structure (bullish or bearish)

        for i in range(lookback // 2, len(candles) - lookback // 2):
            # Check for bullish fractal
            if self.isBullishFractal(highs, i, lookback):
                upperFractal = {'value': highs[i], 'index': i, 'crossed': False}

            # Check for bearish fractal
            if self.isBearishFractal(lows, i, lookback):
                lowerFractal = {'value': lows[i], 'index': i, 'crossed': False}

            # Check crossover above the bullish fractal (ChoCH/BOS Bullish)
            if upperFractal and closes[i] > upperFractal['value'] and not upperFractal['crossed']:
                upperFractal['crossed'] = True
                os = 1  # Set structure to bullish
                return Structure(name="CHOCH", direction="Bullish")

            # Check crossover below the bearish fractal (ChoCH/BOS Bearish)
            if lowerFractal and closes[i] < lowerFractal['value'] and not lowerFractal['crossed']:
                lowerFractal['crossed'] = True
                os = -1  # Set structure to bearish
                return Structure(name="CHOCH", direction="Bearish")
