from typing import Any

from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation


class PDArray:
    def __init__(self, name: str, direction: str):
        self.Ids: list = []
        self.name: str = name
        self.direction: str = direction
        self.assetBrokerStrategyRelation = None

    def addId(self, Id: Any) -> None:
        self.Ids.append(Id)

    def addRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> None:
        self.assetBrokerStrategyRelation = assetBrokerStrategyRelation

    def isIdPresent(self, id_: list) -> Any:
        """
        Check if a specific ID is stored in the 'ids' list.
        """
        if id_ in self.Ids:
            return True
        return False