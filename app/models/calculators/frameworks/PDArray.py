from app.models.calculators.frameworks.FrameWork import FrameWork
from app.monitoring.logging.logging_startup import logger


class PDArray(FrameWork):
    def __init__(self, name: str, direction: str):
        super().__init__("PDArray")
        self.name: str = name
        self.direction: str = direction
        self.candles = []
        self.status = ""

    def add_candles(self, candles) -> None:
        # Efficiently add multiple candles
        self.candles.extend(candles)

    def add_status(self, status) -> None:
        self.status = status

    def is_id_present(self, ids_: list) -> bool:
        """
        Überprüft, ob alle IDs in `self` in der Liste `ids_` enthalten sind.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self` in `ids_` enthalten sind, sonst False
        """
        try:
            candlesIds = [candle.id for candle in self.candles]
            return all(id_ in ids_ for id_ in candlesIds)
        except Exception as e:
            logger.critical(e)
        finally:
            return False

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        try:
            attributes = {
                "typ" : self.typ,
                "timeFrame" : self.timeFrame,
                "name": self.name,
                "direction": self.direction,
                "candles": [candle.to_dict() for candle in self.candles],
                "status": self.status if self.status else None,
            }

            # Filter out attributes with None values
            filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

            return {self.__class__.__name__: filtered_attributes}
        except Exception as e:
            logger.exception(e)
            raise ValueError
