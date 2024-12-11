from typing import Any


class FlyweightFactory:
    _flyweights = {}

    @classmethod
    def getFlyweight(cls, attribute: Any) -> Any:
        """Gibt den Flyweight für das Attribut oder erstellt ihn, falls er nicht existiert."""
        if attribute not in cls._flyweights:
            cls._flyweights[attribute] = attribute  # Speichert den Wert nur einmal
        return cls._flyweights[attribute]
