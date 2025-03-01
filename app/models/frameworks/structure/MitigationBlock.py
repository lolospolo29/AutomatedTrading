from typing import Optional

from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.models.frameworks.structure.StructureEnum import StructureEnum


class MitigationBlock(IConfirmation):

    def __init__(self):
        self.name = StructureEnum.MITIGATIONBLOCK.value

    def return_confirmation(self, candles: list[Candle], lookback: int) -> list[Structure]:
        structures = []

        last_candle: Candle = candles[-1]
        if lookback is not None and len(candles) > lookback:
            candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

        if lookback is not None and len(candles) < lookback:
            return []

        if len(candles) < 2:
            return []

        bullish_a: Optional[Candle, None] = None
        bullish_b: Optional[Candle, None] = None
        bullish_is_valid = False

        last_structure: Optional[Candle, None] = None

        bearish_a: Optional[Candle, None] = None
        bearish_b: Optional[Candle, None] = None
        bearish_is_valid = False

        for candle in candles:

            if candle.close > candle.open:
                if bullish_a is None:
                    bullish_a = candle
                if bullish_a.high < candle.close and bullish_is_valid:
                    if bullish_a.iso_time < bullish_b.iso_time:
                        structure = Structure(name=self.name, direction="Bullish", candles=[bullish_a, bullish_b]
                                              , timeframe=last_candle.timeframe)
                        structures.append(structure)
                        bullish_a = candle
                        bullish_b = None
                        bullish_is_valid = False
                        bearish_a = None
                        bearish_b = None
                        bearish_is_valid = False
                        continue

                if candle.close > bullish_a.high:
                    bullish_a = candle

            if candle.close < candle.open:
                if bearish_a is None:
                    bearish_a = candle
                if bearish_a.low > candle.close and bearish_is_valid:
                    if bearish_a.iso_time < bearish_b.iso_time:
                        structure = Structure(name=self.name, direction="Bearish", candles=[bearish_a, bearish_b]
                                              , timeframe=last_candle.timeframe)
                        structures.append(structure)
                        bullish_a = None
                        bullish_b = None
                        bullish_is_valid = False
                        bearish_a = candle
                        bearish_b = None
                        bearish_is_valid = False
                        continue

                if candle.close < bearish_a.low:
                    bearish_a = candle

            if bullish_b is None:
                bullish_b = candle
            if bearish_b is None:
                bearish_b = candle

            if candle.close < bullish_b.low and bullish_a:
                bullish_b = candle
                bullish_is_valid = True
            if candle.close > bearish_b.high and bearish_a:
                bearish_b = candle
                bearish_is_valid = True

        return structures
