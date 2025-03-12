class TrailingStop:
    """Trail the Stop Loss if 75% in Profit"""

    @staticmethod
    def returnFibonnaciTrailing(currentPrice: float, stop: float, entry: float) -> float:
        level = 0
        if stop < entry < currentPrice:
            level = currentPrice - 0.75 * (currentPrice - entry)
        if stop > entry > currentPrice:
            level = currentPrice + 0.75 * (entry - currentPrice)
        return level
