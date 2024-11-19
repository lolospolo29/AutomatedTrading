from Interfaces.Strategy.IConfirmation import IConfirmation
from Models.Main.Asset.Candle import Candle
from Models.StrategyAnalyse.Structure import Structure


class CISD(IConfirmation):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "CISD"

    def returnConfirmation(self, candles: list[Candle]) -> list:
        if len(candles) < self.lookback:
            return []

        rowCandles = 0
        direction = None
        tracked_structures = []  # List of structures to track their levels
        currentStructure = []
        last_traded_structure = None  # Store the last structure that was traded

        # Extract candle data
        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        for i in range(1, len(close)):
            # Determine the direction of the current candle
            currentDirection = 'Bullish' if close[i] > opens[i] else 'Bearish'

            # Initialize direction on the first candle
            if direction is None:
                direction = currentDirection
                rowCandles = 1
            # Same direction: continue tracking
            elif currentDirection == direction:
                rowCandles += 1
            # Direction changes
            else:
                if rowCandles >= self.lookback:
                    if direction == 'Bearish':
                        tracked_structures.append({
                            "type": "Bearish",
                            "level": max(highs[i - rowCandles:i]),
                            "id": ids[i - 1]
                        })
                    elif direction == 'Bullish':
                        tracked_structures.append({
                            "type": "Bullish",
                            "level": min(lows[i - rowCandles:i]),
                            "id": ids[i - 1]
                        })

                # Reset for the new direction
                direction = currentDirection
                rowCandles = 1

            # Check if any tracked structure is traded through
            for struct in tracked_structures:
                if struct["type"] == "Bearish" and close[i] > struct["level"]:
                    last_traded_structure = Structure(self.name, "Bullish", ids[i])
                    currentStructure.clear()
                    currentStructure.append(last_traded_structure)
                    tracked_structures.remove(struct)  # Remove structure after it is traded through
                elif struct["type"] == "Bullish" and close[i] < struct["level"]:
                    last_traded_structure = Structure(self.name, "Bearish", ids[i])
                    currentStructure.clear()
                    currentStructure.append(last_traded_structure)
                    tracked_structures.remove(struct)  # Remove structure after it is traded through

        # Return the last traded structure
        return currentStructure

