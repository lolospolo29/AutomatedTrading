import random
import string

from files.models.asset.Relation import Relation
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade


class TradeBuilder:
    def __init__(self):
        self.trade = None

    def create_trade(self, relation:Relation, category:str, side:str, orders:list[Order]=None):
        self.trade = Trade()
        self.trade.relation_id = str(relation.relation_id)
        self.trade.category = category

        if orders is None:
            orders = []
        else:
            self.trade.orders = orders#

        self.trade.side = side
        self.trade.trade_id = self._generate_order_link_id(relation.asset, relation.broker, relation.strategy)
        return self

    def build(self):
        return self.trade

    @staticmethod
    def _generate_order_link_id(asset: str, broker: str, strategy: str) -> str:
        """
        Generate a custom orderLinkId with the format:
        yymmddhhmmss-<3_letters_currency>-<3_letters_broker>-<3_letters_strategy>-<order_number>

        Args:
            asset (str): The currency name (e.g., "Bitcoin").
            broker (str): The broker name (e.g., "Binance").
            strategy (str): The strategy name (e.g., "Scalping").
            order_number (int): The order number (e.g., 1).

        Returns:
            str: A formatted orderLinkId.
        """
        from datetime import datetime
        # Current timestamp in the format yymmddhhmmss
        timestamp = datetime.now().strftime("%y%m%d%H%M%S")

        # Take the first 3 letters of the input values, converted to uppercase
        currency_part = asset[:3].upper()
        broker_part = broker[:3].upper()
        strategy_part = strategy[:3].upper()

        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Format the orderLinkId
        order_link_id = f"{timestamp}-{currency_part}-{broker_part}-{strategy_part}-{random_part}"

        return order_link_id
