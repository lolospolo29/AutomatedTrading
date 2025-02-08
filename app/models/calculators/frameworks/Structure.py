from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.FrameWork import FrameWork
from app.monitoring.logging.logging_startup import logger


class Structure(FrameWork):

    def __init__(self, name: str, direction: str, candle: Candle):
        super().__init__("Structure")
        self.name: str = name
        self.direction: str = direction
        self.candle = candle

    def is_id_present(self, ids_: list) -> bool:
        """
        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn `self.id` in `ids_` enthalten ist, sonst False
        """
        for id_ in ids_:
            if id_ == self.candle.id:
                return True
        return False
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        try:
            attributes = {
                "typ" : self.typ,
                "name": self.name,
                "direction": self.direction,
                "candles": self.candle.to_dict(),
            }

            # Filter out attributes with None values
            filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

            return {self.__class__.__name__: filtered_attributes}
        except Exception as e:
            logger.critical(e)
            raise ValueError
