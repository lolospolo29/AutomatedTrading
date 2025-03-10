from files.monitoring.logging.logging_startup import logger


class TrailingStop:
    """Trail the Stop Loss if 75% in Profit"""
    @staticmethod
    def returnFibonnaciTrailing(currentPrice: float, stop: float, entry: float) -> float:
        try:
            logger.info("Calculating Trailing Stop")
            logger.debug("values,{},{},{}".format(currentPrice, stop, entry))
            level = 0
            if stop < entry < currentPrice:
                level = currentPrice - 0.75 * (currentPrice - entry)
            if stop > entry > currentPrice:
                level = currentPrice + 0.75 * (entry - currentPrice)
            return level
        except Exception as e:
            logger.critical("Exception occurred in Trailing Stop: {}".format(e))
