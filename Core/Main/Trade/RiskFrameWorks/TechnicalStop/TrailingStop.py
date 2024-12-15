class TrailingStop():
    def moveExit(self, currentPrice: float, stops: list[float], currentStop: float, direction: str) -> float:
        """
        Passt den Stop dynamisch an, basierend auf der Richtung und Mindestentfernung.

        :param currentPrice: Der aktuelle Preis.
        :param stops: Liste aller verfügbaren möglichen Stop-Werte.
        :param currentStop: Der aktuelle Stop-Wert.
        :param direction: Die Richtung, entweder "bullish" oder "bearish".
        :return: Der neue Stop-Wert oder der aktuelle Stop, falls keine Anpassung möglich ist.
        """
        if direction not in ["bullish", "bearish"]:
            raise ValueError("Direction muss 'bullish' oder 'bearish' sein.")

        # Mindestentfernung vom aktuellen Preis (75 % vom currentPrice)

        # Filter mögliche Stops basierend auf der Richtung
        if direction == "bullish":
            min_distance = currentPrice * 0.75
            # Wähle Stops über dem aktuellen Stop
            valid_stops = [stop for stop in stops if stop > currentStop and stop <= min_distance]
        elif direction == "bearish":
            min_distance = currentPrice * 1.25
            # Wähle Stops unter dem aktuellen Stop
            valid_stops = [stop for stop in stops if stop < currentStop and stop >= min_distance]

        # Finde den besten neuen Stop
        if valid_stops:
            if direction == "bullish":
                return min(valid_stops)  # Der nächste Stop knapp über dem aktuellen
            elif direction == "bearish":
                return max(valid_stops)  # Der nächste Stop knapp unter dem aktuellen

        # Kein neuer Stop gefunden, Rückgabe des aktuellen Stops
        return currentStop

