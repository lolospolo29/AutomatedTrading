from app.models.frameworks.structure.StructureEnum import StructureEnum
from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.monitoring.logging.logging_startup import logger


class CISD(IConfirmation):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = StructureEnum.CHANGEINSTATEOFDELIVERY.value

    def return_confirmation(self, candles: list[Candle]) -> list[Structure]:
        current_structure = []
        try:
            if len(candles) < self.lookback:
                return []

            last_candle:Candle = candles[-1]

            row_candles = 0
            direction = None
            tracked_structures = []  # List of structures to track their levels

            # Extract candle data
            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            for i in range(1, len(close)):
                # Determine the direction of the current candle
                current_direction = 'Bullish' if close[i] > opens[i] else 'Bearish'

                # Initialize direction on the first candle
                if direction is None:
                    direction = current_direction
                    row_candles = 1
                # Same direction: continue tracking
                elif current_direction == direction:
                    row_candles += 1
                # Direction changes
                else:
                    if row_candles >= self.lookback:
                        if direction == 'Bearish':
                            tracked_structures.append({
                                "type": "Bearish",
                                "level": max(highs[i - row_candles:i]),
                                "candles": candles[i - 1]
                            })
                        elif direction == 'Bullish':
                            tracked_structures.append({
                                "type": "Bullish",
                                "level": min(lows[i - row_candles:i]),
                                "candles": candles[i - 1]
                            })

                    # Reset for the new direction
                    direction = current_direction
                    row_candles = 1

                # Check if any tracked structure is traded through
                for struct in tracked_structures:
                    if (struct["type"] == "Bearish" and close[i] > struct["level"]) or (struct["type"] == "Bullish" and close[i] < struct["level"]) :
                        last_traded_structure = Structure(name=self.name, direction=struct["type"] , candle=candles[i],timeframe=last_candle.timeframe)
                        current_structure.clear()
                        current_structure.append(last_traded_structure)
                        tracked_structures.remove(struct)  # Remove structure after it is traded through

                # Return the last traded structure
        except Exception as e:
            logger.error("CISD Confirmation Exception: {}".format(e))
        finally:
            return current_structure

