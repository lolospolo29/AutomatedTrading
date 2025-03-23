from datetime import datetime, timedelta
from enum import Enum
from random import randint
from typing import Optional

from files.models.broker.BrokerOrder import BrokerOrder
from files.models.broker.BrokerPosition import BrokerPosition
from files.models.broker.RequestParameters import RequestParameters
from files.models.asset.Candle import Candle


class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class TimeInForce(Enum):
    GTC = "GTC"  # Good Till Cancelled
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    DAY = "DAY"  # Day order


class FakeHandler:

    def __init__(self):
        self._name = "Faker"
        self._broker_positions: list[BrokerPosition] = []  # List to store active positions
        self._orders: list[BrokerOrder] = []  # List to store active orders

    def return_name(self) -> str:
        return self._name

    def place_order(self, request_params: RequestParameters) -> BrokerOrder:
        """
        Simulate placing an order by filling in the BrokerOrder object with parameters.
        """
        order_id = str(randint(100000, 999999))  # Simulate an order ID

        try:
            order_type = OrderType[request_params.orderType]
            side = Side[request_params.side]
            time_in_force = TimeInForce[request_params.timeInForce]
        except KeyError as e:
            raise ValueError(f"Invalid value for {e}.")

        order = BrokerOrder(
            orderId=order_id,
            symbol=request_params.symbol,
            side=side.value,
            qty=request_params.qty,
            price=request_params.price,
            orderType=order_type.value,
            timeInForce=time_in_force.value,
            orderStatus=OrderStatus.NEW.value,  # Initially set the status to NEW
            createdTime=datetime.utcnow().isoformat(),
            updatedTime=datetime.utcnow().isoformat(),
            orderLinkId=request_params.orderLinkId,
            positionIdx=request_params.positionIdx,
            triggerPrice=request_params.triggerPrice,
            stopLoss=request_params.stopLoss,
            takeProfit=request_params.takeProfit,
            reduceOnly=request_params.reduceOnly,
            closeOnTrigger=request_params.closeOnTrigger,
            cumExecQty=str(0),  # Initially, the cumulative executed quantity is 0
            cumExecValue=str(0),  # Initially, the cumulative executed value is 0
            category="NORMAL",  # Default to "NORMAL" order category
        )

        # Handle order type-specific logic
        if order.orderType == OrderType.LIMIT.value and not order.price:
            raise ValueError("For a LIMIT order, price must be specified.")

        if order.orderType == OrderType.MARKET.value and order.price:
            raise ValueError("For a MARKET order, price should not be specified.")

        self._orders.append(order)

        # Update BrokerPosition after placing the order
        self.update_broker_position(order)

        return order

    def amend_order(self, request_params: RequestParameters) -> BrokerOrder:
        """
        Simulate amending an order with various parameters.
        """
        # Find the order by order ID
        order = next((o for o in self._orders if o.orderId == request_params.orderId), None)
        if not order:
            raise ValueError(f"Order with ID {request_params.orderId} not found.")

        # Ensure the order is not already filled or canceled
        if order.status in [OrderStatus.FILLED.value, OrderStatus.CANCELED.value]:
            raise ValueError(f"Cannot amend an order that is {order.status}.")

        # Amend price or quantity based on the request
        if request_params.price is not None and order.price != request_params.price:
            order.price = request_params.price
            order.updatedTime = datetime.utcnow().isoformat()

        if request_params.qty is not None and order.qty != request_params.qty:
            order.qty = request_params.qty
            order.updatedTime = datetime.utcnow().isoformat()

        # Amend time in force, if provided
        if request_params.timeInForce is not None and order.timeInForce != request_params.timeInForce:
            order.timeInForce = request_params.timeInForce
            order.updatedTime = datetime.utcnow().isoformat()

        # Amend stop loss and take profit if provided
        if request_params.stopLoss is not None:
            order.stopLoss = request_params.stopLoss
        if request_params.takeProfit is not None:
            order.takeProfit = request_params.takeProfit

        # Update position index if provided
        if request_params.positionIdx is not None:
            order.positionIdx = request_params.positionIdx

        # Handle reduceOnly and closeOnTrigger updates
        if request_params.reduceOnly is not None:
            order.reduceOnly = request_params.reduceOnly
        if request_params.closeOnTrigger is not None:
            order.closeOnTrigger = request_params.closeOnTrigger

        # Update trigger price if provided
        if request_params.triggerPrice is not None:
            order.triggerPrice = request_params.triggerPrice

        # Handle status changes if needed
        if order.status == OrderStatus.NEW.value:
            order.status = OrderStatus.PARTIALLY_FILLED.value

        # Return the amended order
        return order

    def update_broker_position(self, order: BrokerOrder):
        """
        Update the BrokerPosition based on the placed.
        If a position with the same symbol and side exists, update it. Otherwise, create a new one.
        """
        existing_position = next(
            (pos for pos in self._broker_positions if
             pos.symbol == order.symbol and pos.side == order.side and pos.category == order.category), None
        )

        if existing_position:
            existing_position: BrokerPosition = existing_position
            # Update the existing position (e.g., increase/decrease quantity, adjust leverage)
            existing_position.size += int(order.qty)
            existing_position.updatedTime = datetime.utcnow().isoformat()

            # Update other fields such as stop loss, take profit, etc.
            if order.stopLoss:
                existing_position.stopLoss = order.stopLoss
            if order.takeProfit:
                existing_position.takeProfit = order.takeProfit
        else:
            # Create a new position if none exists for this symbol and side
            new_position = BrokerPosition(
                symbol=order.symbol,
                side=order.side,
                size=str(order.qty),
                leverage=str(1),
                stopLoss=order.stopLoss,
                takeProfit=order.takeProfit,
                createdTIme=datetime.utcnow().isoformat(),
                updatedTime=datetime.utcnow().isoformat(),
            )
            self._broker_positions.append(new_position)

    def update_orders_by_candle(self, candle: Candle, category: str):
        """
        This method updates orders based on the incoming candle data.
        The method checks if an order is filled or if any conditions are met (stop-loss, take-profit, limit).
        """
        for order in self._orders:
            order: BrokerOrder = order
            if order.symbol != candle.asset or order.category != category:
                continue  # Skip orders for a different asset

            if order.status == OrderStatus.FILLED.value:
                continue  # Skip already filled orders

            # Check if the order is a LIMIT order and the price condition is met
            if order.orderType == 'LIMIT':
                if order.side == 'BUY' and candle.close <= order.price:
                    order.status = OrderStatus.FILLED.value
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()
                elif order.side == 'SELL' and candle.close >= order.price:
                    order.status = OrderStatus.FILLED.value
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()

            # Check if the order is a STOP-LOSS order
            if order.stopLoss is not None:
                if order.side == 'BUY' and candle.close <= order.stopLoss:
                    order.status = OrderStatus.FILLED.value  # Stop-loss triggered for a BUY
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()
                elif order.side == 'SELL' and candle.close >= order.stopLoss:
                    order.status = OrderStatus.FILLED.value  # Stop-loss triggered for a SELL
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()

            # Check if the order is a TAKE-PROFIT order
            if order.takeProfit is not None:
                if order.side == 'BUY' and candle.close >= order.takeProfit:
                    order.status = OrderStatus.FILLED.value  # Take-profit triggered for a BUY
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()
                elif order.side == 'SELL' and candle.close <= order.takeProfit:
                    order.status = OrderStatus.FILLED.value  # Take-profit triggered for a SELL
                    order.cumExecQty = order.qty
                    order.cumExecValue = order.qty * candle.close
                    order.updatedTime = datetime.utcnow().isoformat()

            # If the order is not filled, check if its time in force expired
            if order.status == OrderStatus.NEW.value and order.timeInForce == 'DAY':
                # If the candle time exceeds the order's expiry time, cancel it
                if candle.iso_time > datetime.strptime(order.createdTime, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=24):
                    order.status = OrderStatus.EXPIRED.value
                    order.updatedTime = datetime.utcnow().isoformat()

    def update_positions_from_orders(self):
        """
        Updates broker positions based on the filled orders. This method will:
        - Calculate and update position size, average entry price, and unrealized PnL
        - It will be called once the order is filled (status = 'FILLED').
        """
        for order in self._orders:
            if order.status == OrderStatus.FILLED.value:
                # Find the matching position by symbol and category (buy/sell)
                position = next((p for p in self._broker_positions if
                                 p.symbol == order.symbol and p.side == order.side and p.category == order.category),
                                None)
                if position:
                    self._update_position(position, order)

    @staticmethod
    def _update_position(position: BrokerPosition, order: BrokerOrder):
        """
        Updates position details such as size, average entry price, and unrealized PnL based on the order.
        """
        qty = order.qty
        price = order.price

        # Update position size and average entry price
        if order.side == "BUY":
            new_size = float(position.size) + qty
            new_avg_price = (float(position.avgPrice) * float(position.size) + price * qty) / new_size
            position.size = str(new_size)
            position.avgPrice = str(new_avg_price)
        elif order.side == "SELL":
            new_size = float(position.size) - qty
            position.size = str(new_size)

        # Update unrealized PnL
        position.unrealisedPnl = str((price - float(position.avgPrice)) * float(position.size))

        # Update the timestamp when position changes
        position.updatedTime = datetime.utcnow().isoformat()

    def update_positions_by_candle(self, candle: Candle,category:str):
        """
        Updates positions based on the incoming candle data.
        It checks for orders related to the candle's asset and updates the broker positions.
        """
        for position in self._broker_positions:
            # Update only positions matching the candle's asset (symbol)
            if position.symbol == candle.asset and position.category == candle.category:
                self._update_position_from_candle(position, candle)

    @staticmethod
    def _update_position_from_candle(position: BrokerPosition, candle: Candle):
        """
        Updates position details based on the current market price (candle close).
        """
        # Unrealized PnL based on the candle's close price
        position.unrealisedPnl = str((candle.close - float(position.avgPrice)) * float(position.size))

        # Update the timestamp
        position.updatedTime = candle.iso_time.isoformat()

    def cancel_order(self, request_params: RequestParameters) -> Optional[BrokerOrder]:
        """
        Simulate canceling an order.
        """
        order = next((o for o in self._orders if o.orderId == request_params.orderId), None)
        if order:
            order.status = OrderStatus.CANCELED.value
            # Update BrokerPosition after cancellation (decrease qty or remove position)
            self.update_broker_position(order)
            return order
        return None

    def return_order_history(self, request_params: RequestParameters) -> list[BrokerOrder]:
        """
        Simulate retrieving order history.
        """
        return [order for order in self._orders if
                order.symbol == request_params.symbol and order.status != OrderStatus.NEW.value]