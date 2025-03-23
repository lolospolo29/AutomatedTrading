from files.models.asset.Asset import Asset
from files.models.asset.Candle import Candle
from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.Level import Level
from files.models.frameworks.PDArray import PDArray
from files.models.trade.Trade import Trade

class DTOMapper:

    @staticmethod
    def map_trade_to_dto(trade:Trade)->Trade:

        trade_dto = Trade()
        trade_dto.trade_id = trade.trade_id
        trade_dto.trade_mode = trade.trade_mode
        trade_dto.relationId = trade.relation.id
        trade_dto.category = trade.category
        trade_dto.side = trade.side
        trade_dto.tpsl_mode = trade.tpsl_mode
        trade_dto.unrealised_pnl = trade.unrealised_pnl
        trade_dto.leverage = trade.leverage
        trade_dto.size = trade.size
        trade_dto.trade_mode = trade.trade_mode
        trade_dto.updated_time = trade.updated_time
        trade_dto.created_time = trade.created_time

        return trade_dto

    # noinspection PyTypeChecker
    @staticmethod
    def map_framework_to_dto(framework:FrameWork):
        framework_dto = FrameWorkDTO()

        framework_dto.frameWorkId = framework.id
        framework_dto.name = framework.name
        framework_dto.timeframe = framework.timeframe
        framework_dto.direction = framework.direction
        framework_dto.order_link_id = framework.orderLinkId


        if framework.__class__.__name__ == "PDArray":
            pd :PDArray= framework
            framework_dto.status = pd.status
        if framework.__class__.__name__ == "Level":
            level :Level= framework
            framework_dto.level = level.level
            framework_dto.fib_level = level.fib_level

        framework_dto.type = framework.__class__.__name__

        return framework_dto

    @staticmethod
    def map_candle_to_dto(candle:Candle, framework:FrameWork)->CandleDTO:
        candle_dto = CandleDTO(asset=candle.asset, broker=candle.broker, open=candle.open
                               , high=candle.high, low=candle.low, close=candle.close, iso_time=candle.iso_time
                               , timeframe=candle.timeframe, candleId=candle.id)
        candle_dto.frameWorkId = framework.id

        return candle_dto

    @staticmethod
    def map_asset_to_dto(asset:Asset, asset_class_id:id, asset_id:int)->Asset:
        dto = Asset(name=asset.name, assetClass=asset_class_id, assetId=asset_id)

        return dto