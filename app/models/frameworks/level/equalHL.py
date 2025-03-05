from app.models.frameworks.Level import Level
from app.models.frameworks.PDArray import PDArray


class equalHL:
    """
    technical analysis tool that marks identical price levels on a trading chart using the current time-frame,
    assisting traders in identifying potential support and resistance zones or liquidity draws
    """

    def _detect_equal_lows(self, swings: list[PDArray], timeframe,adr:float) -> list[Level]:
        pass

    def _detect_equal_highs(self, swings: list[PDArray], timeframe,adr:float) -> list[Level]:
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
