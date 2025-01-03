import json
from abc import ABC, abstractmethod
from dataclasses import asdict


class POSTParams(ABC):
    @abstractmethod
    def validate(self):
        pass

    def toDict(self) -> str:
        """Return the dictionary representation of the dataclass as a JSON string."""
        # Create a dictionary from the dataclass, excluding None values
        params_dict = {k: v for k, v in asdict(self).items() if v is not None}

        # Convert the dictionary into a JSON string and wrap it with 'params='
        return json.dumps(params_dict)
