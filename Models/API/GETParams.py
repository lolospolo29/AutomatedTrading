from abc import ABC, abstractmethod
from urllib.parse import urlencode


class GETParams(ABC):
    @abstractmethod
    def validate(self):
        pass
    def toQueryString(self) -> str:
        """Convert the dataclass fields to a URL-encoded query string."""
        # Convert the dataclass to a dictionary and filter out None values
        params_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        # Encode the dictionary into a query string
        return urlencode(params_dict)