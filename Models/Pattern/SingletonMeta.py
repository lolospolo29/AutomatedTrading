from abc import ABCMeta
from typing import Any


class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            # Erzeugt und speichert line neue Instanz, falls noch nicht vorhanden
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]