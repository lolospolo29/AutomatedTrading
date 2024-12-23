
from sklearn.linear_model import SGDClassifier
import numpy as np

from app.helper.ProfitStopAnalyzer import ProfitStopAnalyzer
from app.models.riskCalculations.entry.ratio.Models.ProfitStopEntry import ProfitStopEntry


class StrategyAI:
    def __init__(self, analyzer: ProfitStopAnalyzer):
        self.analyzer = analyzer
        self.model = SGDClassifier(loss="log_loss", max_iter=1, warm_start=True)  # SGDClassifier für inkrementelles Lernen

    def train(self, features: np.ndarray, labels: np.ndarray):
        """Trainiere das Modell mit neuen Daten (inkrementelles Lernen)."""
        self.model.partial_fit(features, labels, classes=np.array(["aggressiv", "moderat", "safe"]))  # Modell mit neuen Daten schrittweise trainieren

    def predict_strategy(self, entries: list, x: int) -> list:
        """Vorhersage der besten Strategie basierend auf dem trainierten Modell."""
        features = self.extract_features(entries)
        predicted_label = self.model.predict([features])[0]
        print(predicted_label)
        # Ausgewählte Strategie ausführen
        if predicted_label == "aggressiv":
            return self.analyzer.maxProfit(entries, x)
        elif predicted_label == "moderat":
            return self.analyzer.midRangeStop(entries, x)
        elif predicted_label == "safe":
            return self.analyzer.lowestEntry(entries, x)

    def extract_features(self, entries: list) -> np.ndarray:
        """Extrahiere Merkmale aus den ProfitStopEntry-Daten."""
        avg_profit = np.mean([e.profit for e in entries])
        avg_stop = np.mean([e.stop for e in entries])
        avg_entry = np.mean([e.entry for e in entries])
        avg_distance = np.mean([abs(e.stop - e.entry) for e in entries])

        return np.array([avg_profit, avg_stop, avg_entry, avg_distance])

entries = [
    ProfitStopEntry(profit=100, stop=90, entry=95),
    ProfitStopEntry(profit=200, stop=80, entry=70),
    ProfitStopEntry(profit=150, stop=85, entry=88),
    ProfitStopEntry(profit=50, stop=100, entry=105),
    ProfitStopEntry(profit=300, stop=75, entry=70),
]
# Beispiel: Datenfeed in einem laufenden System
analyzer = ProfitStopAnalyzer()  # Angenommene ProfitStopEntry-Instanzen
ai = StrategyAI(analyzer)

# Anfangsdaten und Labels für das Modell
initial_features = np.array([ai.extract_features(entries) for _ in entries])
initial_labels = ["moderat", "safe", "aggressiv", "safe", "aggressiv"]

# Modell mit den ersten Daten trainieren
ai.train(initial_features, initial_labels)

# Neue Daten werden laufend hinzugefügt
new_entries = [
    ProfitStopEntry(profit=120, stop=95, entry=90),
    ProfitStopEntry(profit=250, stop=80, entry=85),
]

# Neue Features und Labels für das laufende Training
new_features = np.array([ai.extract_features([entry]) for entry in new_entries])
new_labels = ["aggressiv", "safe"]  # Labels für jedes einzelne Entry


# Das Modell wird mit neuen Daten schrittweise trainiert
ai.train(new_features, new_labels)

# Teste die Vorhersage nach dem Training mit den neuen Daten
print(ai.predict_strategy(new_entries, x=3))

new_entries = [
    ProfitStopEntry(profit=1200, stop=150, entry=700),
    ProfitStopEntry(profit=1000, stop=200, entry=500),
]
print(ai.predict_strategy(new_entries, x=1))


# Fitdaten anlegen mit strategy, bester entry und alles ausprobieren von ProfitStopAnalyzer für Training

