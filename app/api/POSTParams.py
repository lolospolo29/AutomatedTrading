import json
from abc import ABC, abstractmethod
from dataclasses import asdict


class POSTParams(ABC):
    """
    Represents an abstract base class for POST request parameters.

    This class serves as a base for all POST request parameter containers.
    It is intended to enforce the implementation of parameter validation
    in derived classes, as well as to provide a standardized way to convert
    the parameters into a JSON string format.
    """
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self) -> str:
        """Return the dictionary representation of the dataclass as a JSON string."""
        # Create a dictionary from the dataclass, excluding None values
        params_dict = {k: v for k, v in asdict(self).items() if v is not None}

        # Convert the dictionary into a JSON string and wrap it with 'params='
        return json.dumps(params_dict)
