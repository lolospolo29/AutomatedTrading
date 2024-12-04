from abc import ABC, abstractmethod
from dataclasses import asdict


class POSTParams(ABC):
    @abstractmethod
    def validate(self):
        pass
    def toDict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

