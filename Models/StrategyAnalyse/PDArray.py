from typing import Any


class PDArray:
    def __init__(self, name: str, direction: str):
        self.Ids: list = []
        self.name: str = name
        self.direction: str = direction

    def addId(self, Id: Any) -> None:
        self.Ids.append(Id)

    def isIdPresent(self, id_: list) -> Any:
        """
        Check if a specific ID is stored in the 'ids' list.
        """
        return id_ in self.Ids
