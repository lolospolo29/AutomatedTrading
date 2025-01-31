import threading

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure
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

    def remove_structure(self, candles: list[Candle], timeFrame: int) -> None:
        with self._lock:
            try:
                _ids = [candle.id for candle in candles]
                structures = self.structures
                for structure in structures:
                    if structure.timeframe == timeFrame:
                        if not structure.is_id_present(_ids):
                            self.structures.remove(structure)
            except Exception as e:
                logger.error("Remove Structure Error", e)

    @staticmethod
    def _compare_structure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.name == structure2.name and structure1.candle.id == structure2.candle.id
                and structure1.direction == structure2.direction):
            return True
        return False
