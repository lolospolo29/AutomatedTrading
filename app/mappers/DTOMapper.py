import uuid
from sqlite3 import Binary

from app.db.mongodb.dtos.AssetDTO import AssetDTO
from app.db.mongodb.dtos.CandleFrameWorkDTO import CandleFrameWorkDTO
from app.db.mongodb.dtos.FrameWorkDTO import FrameWorkDTO
from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.models.asset.Asset import Asset
from app.models.asset.Candle import Candle
from app.models.frameworks.FrameWork import FrameWork
from app.models.frameworks.Level import Level
from app.models.frameworks.PDArray import PDArray
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class DTOMapper:

    @staticmethod
    def map_trade_to_dto(trade:Trade)->TradeDTO:

        trade_dto = TradeDTO()
        trade_dto.tradeId = trade.id
        trade_dto.tradeMode = trade.tradeMode
        trade_dto.relationId = trade.relation.id
        trade_dto.category = trade.category
        trade_dto.side = trade.side
        trade_dto.tpslMode = trade.tpslMode
        trade_dto.unrealisedPnl = trade.unrealisedPnl
        trade_dto.leverage = trade.leverage
        trade_dto.size = trade.size
        trade_dto.tradeMode = trade.tradeMode
        trade_dto.updatedTime = trade.updatedTime
        trade_dto.createdTime = trade.createdTime

        return trade_dto

    # noinspection PyTypeChecker
    @staticmethod
    def map_framework_to_dto(framework:FrameWork):
        framework_dto = FrameWorkDTO()

        framework_dto.frameWorkId = framework.id
        framework_dto.name = framework.name
        framework_dto.timeframe = framework.timeframe
        framework_dto.direction = framework.direction
        framework_dto.orderLinkId = framework.orderLinkId


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
    def map_candle_to_dto(candle:Candle, framework:FrameWork)->CandleFrameWorkDTO:
        candle_dto = CandleFrameWorkDTO(asset=candle.asset,broker=candle.broker,open=candle.open
                                        ,high=candle.high,low=candle.low,close=candle.close,iso_time=candle.iso_time
                                        ,timeframe=candle.timeframe,candleId=candle.id)
        candle_dto.frameWorkId = framework.id

        return candle_dto

    @staticmethod
    def map_asset_to_dto(asset:Asset,asset_class_id:id,asset_id:int)->AssetDTO:
        dto = AssetDTO(name=asset.name,assetClass=asset_class_id,assetId=asset_id)

        return dto



