from app.db.mongodb.dtos.TradeDTO import TradeDTO
from app.models.trade.Trade import Trade


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
