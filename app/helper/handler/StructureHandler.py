import threading

from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.monitoring.logging.logging_startup import logger


class StructureHandler:

    def __init__(self):
        self.structures: list[Structure] = []
        self._lock = threading.Lock()

    def add_structure(self, newStructure: Structure) -> None:
        with self._lock:
            try:
                for structure in self.structures:
                    if self._compare_structure(newStructure, structure):
                        return
                self.structures.append(newStructure)
            except Exception as e:
                logger.error("Add Structure Error", e)

    def return_structure(self) -> list[Structure]:
        with self._lock:
            return self.structures

    def remove_structure(self, candles: list[Candle], timeframe: int) -> None:
        with self._lock:
            try:
                _ids = [candle.id for candle in candles]
                pdArrays = self.structures.copy()
                for structure in pdArrays:
                    structure:Structure = structure
                    if structure.timeframe == timeframe:
                        if not  structure.candle.id in _ids:  # Ensures every `id` in `ids` exists in `_ids`
                            self.structures.remove(structure)
            except Exception as e:
                logger.error("Remove Structure Error", e)

    @staticmethod
    def _compare_structure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.name == structure2.name and structure1.candle.id == structure2.candle.id
                and structure1.direction == structure2.direction):
            return True
        return False
