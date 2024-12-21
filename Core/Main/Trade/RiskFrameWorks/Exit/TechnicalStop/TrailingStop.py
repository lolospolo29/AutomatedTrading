class TrailingStop:
    @staticmethod
    def returnFibonnaciTrailing(currentPrice: float, stop: float, entry: float) -> float:
        level = 0
        if stop < entry < currentPrice:
            level = currentPrice - 0.72 * (currentPrice - entry)
        if stop > entry > currentPrice:
            level = currentPrice + 0.72 * (entry - currentPrice)
        return level


tr = TrailingStop()
print(tr.returnFibonnaciTrailing(80, 130, 126, ))

