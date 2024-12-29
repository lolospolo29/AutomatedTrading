from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.models.trade.Order import Order


class BybitMapper:

    @staticmethod
    def mapOrderToOpenAndClosedOrders (order: Order,baseCoin:str=None,settleCoin:str=None,openOnly:OpenOnlyEnum=None
                                 ,limit:int=20,cursor:str=None) ->OpenAndClosedOrders:
        try:
            # Extract PlaceOrder fields
            fieldsMapped = OpenAndClosedOrders.__annotations__

            # Prepare data for PlaceOrder initialization
            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            open = OpenAndClosedOrders(**mappingData)
            if baseCoin is not None:
                open.baseCoin = baseCoin
            if settleCoin is not None:
                open.settleCoin = settleCoin
            if openOnly is not None:
                open.openOnly = openOnly.value
            if limit is not None:
                open.limit = limit
            if cursor is not None:
                open.cursor = cursor

            return open
        except Exception as e:
            print(e)

    @staticmethod
    def mapOrderToPositionInfo(order: Order,baseCoin:str=None,settleCoin:str=None
                                 ,limit:int=20,cursor:str=None):
        try:
            # Extract PlaceOrder fields
            fieldsMapped = PositionInfo.__annotations__

            # Prepare data for PlaceOrder initialization
            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            open = PositionInfo(**mappingData)
            if baseCoin is not None:
                open.baseCoin = baseCoin
            if settleCoin is not None:
                open.settleCoin = settleCoin
            if limit is not None:
                open.limit = limit
            if cursor is not None:
                open.cursor = cursor

            return open
        except Exception as e:
            print(e)

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
