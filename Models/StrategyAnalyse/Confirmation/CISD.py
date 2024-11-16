from Interfaces.Strategy.IConfirmation import IConfirmation
from Models.Main.Asset.Candle import Candle
from Models.StrategyAnalyse.Level import Level
from Models.StrategyAnalyse.Structure import Structure


class CISD(IConfirmation):
    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "CISD"

    def returnConfirmation(self, candles: list[Candle]):

        if len(candles) < self.lookback:
            return False

        rowCandles = 0
        direction = None

        liquidityVoids = []

        opens = [candle.open for candle in candles]
        highs = [candle.high for candle in candles]
        lows = [candle.low for candle in candles]
        close = [candle.close for candle in candles]
        ids = [candle.id for candle in candles]

        # Loop through all candles in the data
        for i in range(1, len(close)):
            # Check if the current candle is bullish or bearish
            currentDirection = 'Bullish' if close[i] > opens[i] else 'Bearish'

            # If it's the first candle, set the direction
            if direction is None:
                direction = currentDirection
                rowCandles = 1
            # If the current candle is in the same direction as the previous one
            elif currentDirection == direction:
                rowCandles += 1
            # If the direction changes
            else:
                # If there are enough candles in the row, create a new PDArray
                if rowCandles >= self.lookback:
                    # Add the candle data to the PDArray
                    stateId = None
                    level = -1

                    for j in range(i - rowCandles, i):
                        if direction == 'Bullish':
                            self.checkStructure(direction,level,stateId,highs[j],ids[j])
                        if direction == 'Bearish':
                            self.checkStructure(direction, level, stateId, lows[j], ids[j])

                    struct = Level(self.name,level)
                    struct.direction = currentDirection
                    liquidityVoids.append(struct)

                # Reset for the new direction
                direction = currentDirection
                rowCandles = 1

        if len(liquidityVoids) > 0:
            direction = "Bullish"
            id = -1
            for candle in candles:
                for liquidityVoid in liquidityVoids:
                    if liquidityVoid.direction == 'Bullish':
                        if candle.high > liquidityVoid.level:
                            direction = "Bullish"
                            id = candle.id
                    if liquidityVoid.direction == 'Bearish':
                        if candle.low < liquidityVoid.level:
                            direction = "Bearish"
                            id = candle.id
            return Structure(self.name,direction,id)


    @staticmethod
    def checkStructure(direction, level, id, candleLevel, candleId):
        if direction == 'Bullish':
            if level is None:
                stateId = candleId
                level = candleLevel
                return level,stateId
            if level < candleLevel:
                stateId = candleId
                level = candleLevel
                return level,stateId
        if direction == 'Bearish':
            if level is None:
                stateId = candleId
                level = candleLevel
                return level,stateId
            if level > candleLevel:
                stateId = candleId
                level = candleLevel
                return level,stateId
        return level,id
