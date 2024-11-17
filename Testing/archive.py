import json
import os
from datetime import datetime

import pandas as pd

# Pfade definieren
observed_folder = r"C:\AutomatedTrading\ObservedFolder\archive"
# Sicherstellen, dass der Archivordner existiert

# Alle Dateien im ObservedFolder iterieren
# Alle Dateien im ObservedFolder iterieren
for filename in os.listdir(observed_folder):
    file_path = os.path.join(observed_folder, filename)

    # Nur CSV-Dateien verarbeiten
    if not filename.endswith(".csv"):
        continue

    print(f"Verarbeite Datei: {filename}")

    # CSV-Datei einlesen
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        print(f"Fehler beim Einlesen von {filename}: {e}")
        continue

    # Daten nach Asset-Typ und Datum filtern
    for _, row in data.iterrows():
        try:
            # JSON aus der "Description"-Spalte extrahieren
            description_json = row["Description"]
            candle_data = json.loads(description_json)
            asset = candle_data["Candle"]["asset"]
            iso_time = candle_data["Candle"]["IsoTime"]

            # Datum aus IsoTime extrahieren
            date = datetime.strptime(iso_time.rstrip("Z"), "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')

            # Ordnerstruktur: archive/<asset>/<date>
            asset_folder = os.path.join(observed_folder, asset, date)
            os.makedirs(asset_folder, exist_ok=True)

            # Datei für das Datum erstellen oder anhängen
            asset_file_path = os.path.join(asset_folder, f"{asset}_{date}.csv")
            with open(asset_file_path, "a") as f:
                f.write(",".join(map(str, row.values)) + "\n")  # Originalzeile speichern
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Zeile in {filename}: {e}")
            continue

    print(f"Verarbeitung von {filename} abgeschlossen.")

print("Alle Dateien erfolgreich verarbeitet.")
