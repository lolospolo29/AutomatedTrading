from abc import ABC, abstractmethod


class ResponseParams(ABC):
        @abstractmethod
        def jsonMapToClass(self):
            pass