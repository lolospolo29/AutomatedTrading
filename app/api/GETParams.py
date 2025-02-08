from abc import ABC, abstractmethod
from urllib.parse import urlencode


class GETParams(ABC):
    """
    Abstract base class that represents a set of parameters to be sent
    in a GET request. This class enforces the implementation of a validation
    method and provides a utility to convert the parameters into a
    URL-encoded query string.

    """
    @abstractmethod
    def validate(self):
        pass

    def to_query_string(self) -> str:
        """Convert the dataclass fields to a URL-encoded query string."""
        # Convert the dataclass to a dictionary and filter out None values
        params_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        # Encode the dictionary into a query string
        return urlencode(params_dict)
