from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level

class equalHL:
    """
    technical analysis tool that marks identical price levels on a trading chart using the current time-frame,
    assisting traders in identifying potential support and resistance zones or liquidity draws
    """
    @staticmethod
    def _findMedian(values:list[float]):
        sums = sum(values)
        return sums/len(values)

    def _calculateThreshold(self, prices:list[float]):
        prev_price = 0
        differences = []
        for price in prices:
            if prev_price == 0:
                prev_price = price
            if prev_price != price:
                differences.append(abs(price - prev_price))
                prev_price = price
        if differences:
            return self._findMedian(differences)

    def _detect_equal_lows(self, candles: list[Candle], timeframe) -> list[Level]:
        pass

    def _detect_equal_highs(self, candles: list[Candle], timeFrame) -> list[Level]:
        pass

    def _filter_levels(self, levels: list[Level]) -> list[Level]:
        """
        Filters the detected equal levels to retain only the most significant level
        (lowest for lows, highest for highs) within the same threshold range.
        """
        if not levels:
            return levels

        filteredLevels = []
        levels.sort(key=lambda x: x.level)  # Sort by price level
        levelsValue = [level.level in levels for level in levels]

        threshold = self._calculateThreshold(levelsValue)

        currentGroup = [levels[0]]  # Start with the first level

        for i in range(1, len(levels)):
            # If the current level is within the threshold range of the previous, group them together
            if abs(levels[i].level - currentGroup[-1].level) < threshold:
                currentGroup.append(levels[i])
            else:
                # If a new group starts, filter the current group and add to the result
                filteredLevels.append(self._get_significant_level(currentGroup))
                currentGroup = [levels[i]]

        # Handle the last group
        if currentGroup:
            filteredLevels.append(self._get_significant_level(currentGroup))

        return filteredLevels

    @staticmethod
    def _get_significant_level(levels: list[Level]) -> Level:
        """
        Returns the most significant level from a list of levels.
        For lows, this is the lowest level.
        For highs, this is the highest level.
        """
        # For equal lows, we take the lowest level
        if levels[0].name == "EqualLow":
            return min(levels, key=lambda x: x.level)
        # For equal highs, we take the highest level
        else:
            return max(levels, key=lambda x: x.level)
