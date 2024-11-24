from typing import Any

from Models.RiskManagement.Invalidation.InvalidationClose import InvalidationClose
from Models.RiskManagement.Invalidation.InvalidationSteady import InvalidationSteady
from Models.RiskManagement.Martingale.AntiMartingale import AntiMartingale
from Models.RiskManagement.Martingale.Martingale import Martingale
from Models.RiskManagement.OrderWeightage.OrderWeightage import OrderWeightage
from Models.RiskManagement.Ratio.FixedRatio import FixedRatio
from Models.RiskManagement.Ratio.RangeRatio import RangeRatio
from Models.RiskManagement.StrategicStop.EndOfmbalance import EndOfImbalance
from Models.RiskManagement.StrategicStop.OBStop import OBStop
from Models.RiskManagement.StrategicStop.Swing import SwingStop
from Models.RiskManagement.TechnicalEntry.CE import CE
from Models.RiskManagement.TechnicalEntry.Drill import DrillEntry
from Models.RiskManagement.TechnicalEntry.Fill import FillEntry
from Models.RiskManagement.TechnicalStop.BreakEven import BreakEven
from Models.RiskManagement.TechnicalStop.TrailingStop import TrailingStop


class RiskMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RiskMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.invalidationClose: InvalidationClose = InvalidationClose()
            self.invalidationSteady: InvalidationSteady = InvalidationSteady()
            self.antiMartingale: AntiMartingale = AntiMartingale()
            self.martingale: Martingale = Martingale()
            self.orderWeightage: OrderWeightage = OrderWeightage()
            self.fixedRatio: FixedRatio = FixedRatio()
            self.rangeRatio: RangeRatio = RangeRatio()
            self.endOfImbalance: EndOfImbalance = EndOfImbalance()
            self.obStop: OBStop = OBStop()
            self.swingStop: SwingStop= SwingStop()
            self.ce: CE = CE()
            self.drill: DrillEntry = DrillEntry()
            self.fill: FillEntry = FillEntry()
            self.be: BreakEven = BreakEven(0.75)
            self.trailingStop: TrailingStop = TrailingStop()
            self.initialized: bool = True  # Mark as initialized

    def calculateRisk(self,riskType,*args, **kwargs) -> Any:

        if riskType == "Close" or riskType == "Steady":
            stopLoss = kwargs['stopLoss']
            candle = kwargs['candle']
            tradeDirection = kwargs['tradeDirection']
            if riskType == "Close":
                return self.invalidationClose.checkInvalidation(stopLoss,candle,tradeDirection)
            if riskType == "Steady":
                return self.invalidationSteady.checkInvalidation(stopLoss, candle, tradeDirection)

        if riskType == "MartingaleOrder":
            ratio = kwargs['ratio']
            mode = kwargs['mode']
            return self.martingale.getOrderAmount(ratio, mode)

        if riskType == "MartingaleModel":
            currentDrawdown = kwargs['currentDrawdown']
            return self.martingale.getMartingaleModel(currentDrawdown)

        if riskType == "AntiMartingaleOrder":
            ratio = kwargs['ratio']
            mode = kwargs['mode']
            return self.antiMartingale.getOrderAmount(ratio, mode)

        if riskType == "AntiMartingaleModel":
            currentDrawdown = kwargs['currentDrawdown']
            return self.antiMartingale.getMartingaleModel(currentDrawdown)

        if riskType == "OrderWeightageTPLevel":
            orderAmount = kwargs['orderAmount']
            tpLevel = kwargs['tpLevel']
            direction = kwargs['direction']
            mode = kwargs['mode']
            return self.orderWeightage.sortOrderToTPLevel(orderAmount,tpLevel,direction,mode)

        if riskType == "OrderWeightagePercentage":
            percentage = kwargs['percentage']
            order_tp_assignments = kwargs['order_tp_assignments']
            mode = kwargs['mode']
            return self.orderWeightage.getPercentagePerLevel(percentage,order_tp_assignments,mode)

        if riskType == "FixedRatio":
            stop = kwargs['stop']
            ratio = kwargs['ratio']
            return self.fixedRatio.getRatio(stop,ratio)

        if riskType == "RangeRatio":
            stop = kwargs['stop']
            takeProfits = kwargs['takeProfits']
            range = kwargs['range']
            return self.rangeRatio.getRatio(stop, takeProfits, range)

        if riskType == "EndOfImbalance":
            candle = kwargs['candle']
            return self.endOfImbalance.getStrategyStop(candle)

        if riskType == "OBStop":
            candle = kwargs['candle']
            mode = kwargs['mode']
            return self.obStop.getStrategyStop(candle, mode)

        if riskType == "Swing":
            candle = kwargs['candle']
            return self.swingStop.getStrategyStop(candle)

        if riskType == "CE":
            candle = kwargs['candle']
            return self.ce.getEntry(candle)

        if riskType == "Drill":
            candle = kwargs['candle']
            return self.drill.getEntry(candle)

        if riskType == "Fill":
            candle = kwargs['candle']
            return self.fill.getEntry(candle)

        if riskType == "BE":
            currentPrice = kwargs['currentPrice']
            entry = kwargs['entry']
            takeProfit = kwargs['takeProfit']
            return self.be.moveExit(currentPrice, entry, takeProfit)

        if riskType == "TrailingStop":
            currentPrice = kwargs['currentPrice']
            stops = kwargs['stops']
            currentStop = kwargs['currentStop']
            direction = kwargs['direction']
            return self.trailingStop.moveExit(currentPrice, stops, currentStop, direction)
