from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure


class Choch(IConfirmation):

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "CHOCH"

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

    def returnConfirmation(self, candles: list[Candle]) -> list[Structure]:
        """
        Identify Change of Character (ChoCH) from provided data.
        _param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'Choch_Bullish', 'Choch_Bearish' or None.
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

        upperFractal = None
        lowerFractal = None
        os = 0  # Keeps track of the order of structure (bullish or bearish)

        for i in range(self.lookback // 2, len(candles) - self.lookback // 2):
            # Check for bullish fractal
            if self.isBullishFractal(highs, i, self.lookback):
                upperFractal = {'value': highs[i], 'index': i, 'crossed': False}

            # Check for bearish fractal
            if self.isBearishFractal(lows, i, self.lookback):
                lowerFractal = {'value': lows[i], 'index': i, 'crossed': False}

            # Check crossover above the bullish fractal (ChoCH/BOS Bullish)
            if upperFractal and closes[i] > upperFractal['value'] and not upperFractal['crossed']:
                upperFractal['crossed'] = True
                os = 1  # Set structure to bullish

                structure =  Structure(name=self.name, direction="Bullish", candle=candles[i])
                structures.append(structure)

            # Check crossover below the bearish fractal (ChoCH/BOS Bearish)
            if lowerFractal and closes[i] < lowerFractal['value'] and not lowerFractal['crossed']:
                lowerFractal['crossed'] = True
                os = -1  # Set structure to bearish
                structure =  Structure(name=self.name, direction="Bearish", candle=candles[i])
                structures.append(structure)

        return structures
