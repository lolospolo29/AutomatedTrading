from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level

class Fibonnaci:

    def __init__(self,levels:list[float],name:str):
        self.retracement_levels: list[float] = levels
        self.name = name

    def return_levels(self, highest_candle:Candle,lowest_candle:Candle) -> list[Level]:
        """
        Projects the High and the Low of the given Candles with Lookback
        :param lowest_candle:
        :param highest_candle:
        """
        all_levels = []
        try:
            levels = self._generate_fib_levels_bullish(highest_candle,lowest_candle)
            all_levels.extend(levels)
            levels = self._generate_fib_levels_bearish(highest_candle,lowest_candle)
            all_levels.extend(levels)

        except Exception as e:
            pass
        finally:
            return all_levels

    def _generate_fib_levels_bullish(self,highest_candle:Candle,lowest_candle:Candle) -> list[Level]:
        levels = []
        for fib_level in self.retracement_levels:
            bullish_level = highest_candle.high - fib_level * (highest_candle.high - lowest_candle.low)
            levels.append(Level(name=self.name, level=bullish_level
                                ,fib_level=fib_level,direction="Bullish",timeframe=highest_candle.timeframe
                                ,candles=[highest_candle,lowest_candle]))
        return levels

    def _generate_fib_levels_bearish(self,highest_candle:Candle,lowest_candle:Candle) -> list[Level]:
        levels = []
        for fib_level in self.retracement_levels:
            bearish_level = lowest_candle.low + fib_level  * (highest_candle.high - lowest_candle.low)
            levels.append(Level(name=self.name, level=bearish_level,fib_level=fib_level,
                                candles=[highest_candle,lowest_candle]
                                ,direction="Bearish",timeframe=highest_candle.timeframe))
        return levels