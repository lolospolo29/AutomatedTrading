class Level:
    def __init__(self, name: str, level: float):
        self.name: str = name
        self.level: float = level
        self.fibLevel = None
        self.direction = None
        self.ids = []

    def setFibLevel(self, fibLevel: float, direction: str, ids: list):
        self.fibLevel = fibLevel
        self.direction = direction
        for id in ids:
            self.ids.append(id)
