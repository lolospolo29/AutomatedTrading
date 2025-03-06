from app.models.frameworks.Level import Level
from app.models.frameworks.PDArray import PDArray


class equalHL:
    """
    technical analysis tool that marks identical price levels on a trading chart using the current time-frame,
    assisting traders in identifying potential support and resistance zones or liquidity draws
    """
    def detect_equal_hl(self,swings:list[PDArray], adr:float):

        levels = []

        highs = [swing for swing in swings if swing.name == "High"]
        low = [swing for swing in swings if swing.name == "Low"]

        levels.extend(self._filter_highs(low,adr))
        levels.extend(self._filter_lows(highs,adr))

        return levels

    @staticmethod
    def _filter_highs(swings: list[PDArray], adr: float) -> list[Level]:
        """Helper function to find swings that are within ADR range."""
        levels = []

        for i, swing1 in enumerate(swings):
            swing1:PDArray = swing1
            for j, swing2 in enumerate(swings):
                if i >= j:  # Avoid duplicate comparisons
                    continue

                swing1_high:float = max(candle.high for candle in swing1.candles)
                swing2_high:float = max(candle.high for candle in swing2.candles)

                highest = max(swing1_high, swing2_high)

                # Check if the highs/lows are within ADR tolerance
                if abs(swing1_high - swing2_high) <= adr:
                    levels.append(Level(level=highest,fib_level=0,candles=[],reference=swing1.id,name="EQH"))

        return levels

    @staticmethod
    def _filter_lows(swings: list[PDArray], adr: float) -> list[Level]:
        """Helper function to find swings that are within ADR range."""
        levels = []

        for i, swing1 in enumerate(swings):
            swing1: PDArray = swing1
            for j, swing2 in enumerate(swings):
                if i >= j:  # Avoid duplicate comparisons
                    continue

                swing1_low = max(candle.low for candle in swing1.candles)
                swing2_low = max(candle.low for candle in swing2.candles)

                lowest = min(swing1_low, swing2_low)

                # Check if the highs/lows are within ADR tolerance
                if abs(swing1_low - swing2_low) <= adr:
                    levels.append(
                        Level(level=lowest, fib_level=0, candles=[],
                              reference=swing1.id,name="EQL"))

        return levels

    @staticmethod
    def _filter_levels(levels:list[Level], adr: float) -> list[Level]:
        pass
