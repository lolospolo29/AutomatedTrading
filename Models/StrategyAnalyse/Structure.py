from typing import Any


class Structure:
    def __init__(self, name: str, direction: str, id : Any):
        self.name: str = name
        self.direction: str = direction
        self.id = id
