from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.models.trade.Order import Order


class BybitMapper:

    @staticmethod
    def mapOrderToPlaceOrder(order: Order)-> PlaceOrder:
        try:
            # Extract PlaceOrder fields
            placeorder_fields = PlaceOrder.__annotations__

            # Prepare data for PlaceOrder initialization
            placeorder_data = {}
            for field in placeorder_fields:
                if hasattr(order, field):
                    placeorder_data[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            return PlaceOrder(**placeorder_data)
        except Exception as e:
            print(e)
