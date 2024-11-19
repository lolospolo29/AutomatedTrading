from Models.StrategyAnalyse.FrameWork import FrameWork


class Level(FrameWork):
    def __init__(self, name: str, level: float):
        super().__init__("Level")
        self.name: str = name
        self.direction = None
        self.level: float = level
        self.fibLevel = None
        self.ids: list= []

    def setFibLevel(self, fibLevel: float, direction: str, ids: list):
        self.fibLevel = fibLevel
        self.direction = direction
        for id in ids:
            self.ids.append(id)

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob alle IDs in `self.Ids` in der Liste `ids_` enthalten sind.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self.Ids` in `ids_` enthalten sind, sonst False
        """
        return all(id_ in ids_ for id_ in self.ids)
