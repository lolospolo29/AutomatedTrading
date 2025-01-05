from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.enums.OrderFilterEnum import OrderFilterEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.post.AddOrReduceMargin import AddOrReduceMargin
from app.api.brokers.bybit.post.AmendOrder import AmendOrder
from app.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from app.api.brokers.bybit.post.CancelOrder import CancelOrder
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.api.brokers.bybit.post.SetLeverage import SetLeverage
from app.models.trade.CategoryEnum import CategoryEnum
from app.models.trade.Order import Order


class BybitMapper:

    # region Order To GET Mapping
    @staticmethod
    def mapOrderToOpenAndClosedOrders (order: Order,baseCoin:str=None,settleCoin:str=None,openOnly:OpenOnlyEnum=None
                                 ,limit:int=20,cursor:str=None) ->OpenAndClosedOrders:
        try:
            fieldsMapped = OpenAndClosedOrders.__annotations__

            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            mappedObject = OpenAndClosedOrders(**mappingData)
            if baseCoin is not None:
                mappedObject.baseCoin = baseCoin
            if settleCoin is not None:
                mappedObject.settleCoin = settleCoin
            if openOnly is not None:
                mappedObject.openOnly = openOnly.value
            if limit is not None:
                mappedObject.limit = limit
            if cursor is not None:
                mappedObject.cursor = cursor

            return mappedObject
        except Exception as e:
            print(e)

    @staticmethod
    def mapOrderToPositionInfo(order: Order,baseCoin:str=None,settleCoin:str=None
                                 ,limit:int=20,cursor:str=None)->PositionInfo:
        try:
            # Extract PlaceOrder fields
            fieldsMapped = PositionInfo.__annotations__

            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            mappedObject = PositionInfo(**mappingData)
            if baseCoin is not None:
                mappedObject.baseCoin = baseCoin
            if settleCoin is not None:
                mappedObject.settleCoin = settleCoin
            if limit is not None:
                mappedObject.limit = limit
            if cursor is not None:
                mappedObject.cursor = cursor

            return mappedObject
        except Exception as e:
            print(e)
    # endregion

    @staticmethod
    def mapOrderToModifyMargin(order: Order,margin:str=None)->AddOrReduceMargin:
        try:
            fieldsMapped = AddOrReduceMargin.__annotations__

            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            mappedObject = AddOrReduceMargin(**mappingData)
            if margin is not None:
                mappedObject.margin = margin

            return mappedObject
        except Exception as e:
            print(e)

    @staticmethod
    def mapOrderToAmendOrder(order: Order)->AmendOrder:
        try:
            fieldsMapped = AmendOrder.__annotations__

            mappingData = {}
            for field in fieldsMapped:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            mappedObject = AmendOrder(**mappingData)

            return mappedObject
        except Exception as e:
            print(e)

    @staticmethod
    def mapInputToCancelAllOrders(category:CategoryEnum=None,symbol:str=None,baseCoin:str=None,settleCoin:str=None,
                        orderFilter:OrderFilterEnum=None,stopOrderType:bool=False):
        try:
            mappedObject = CancelAllOrders(str(category.value))
            if symbol is not None:
                mappedObject.symbol = symbol
            if baseCoin is not None:
                mappedObject.baseCoin = baseCoin
            if settleCoin is not None:
                mappedObject.settleCoin = settleCoin
            if orderFilter is not None:
                mappedObject.orderFilter = orderFilter.value
            if stopOrderType:
                mappedObject.stopOrderType = 'Stop'
            return mappedObject
        except Exception as e:
            print(e)
    @staticmethod
    def mapOrderToCancelOrder(order:Order)->CancelOrder:
        try:
            # Extract PlaceOrder fields
            mappedFields = CancelOrder.__annotations__

            # Prepare data for PlaceOrder initialization
            mappingData = {}
            for field in mappedFields:
                if hasattr(order, field):
                    mappingData[field] = getattr(order, field)
                else:
                    continue
            # Instantiate PlaceOrder
            return CancelOrder(**mappingData)
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

    @staticmethod
    def mapInputToSetLeverage(category:CategoryEnum=None,symbol:str=None,buyLeverage:str=None,sellLeverage:str=None):
        try:
            mappedObject = SetLeverage(category=str(category.value),symbol=symbol,buyLeverage=buyLeverage,sellLeverage=sellLeverage)
            return mappedObject
        except Exception as e:
            print(e)
