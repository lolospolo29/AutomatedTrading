import os
import threading
import json
from typing import Any
from configparser import ConfigParser
from dotenv import load_dotenv
from files.monitoring.logging.logging_startup import logger

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()


class SecretsManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SecretsManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing
    def __init__(self, config_file=None):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            try:
                config_file = os.getenv("CONFIG_PATH", config_file)  # Holen von CONFIG_PATH
                self._config_file = config_file
                self._secrets_file_path = self.load_secrets_path()  # Laden des Geheimnis-Pfades
                self._secrets = self.load_secrets()  # Laden der Geheimnisse
                self._initialized = True  # Markiere als initialisiert
            except Exception as e:
                logger.exception(f"Failed to load secrets file: {e}")

    # endregion

    # region Secrets Functions
    def load_secrets_path(self) -> Any:
        """Lade den Pfad zur Secrets-Datei aus der Konfigurationsdatei."""
        environment_path_key = f"SECRETS_PATH_{os.getenv('ENV', 'DEV').upper()}"
        config = ConfigParser()

        # Lade die Konfigurationsdatei und suche den spezifischen Pfad
        if self._config_file:
            config.read(self._config_file)
        else:
            config.read(os.getenv("CONFIG_PATH", "config.ii"))  # Fallback auf "config.ini"

        secrets_path = config.get("paths", environment_path_key, fallback="config/secrets.json")

        # Rückgabe des vollständigen Pfads zur Secrets-Datei
        return os.path.join(os.path.dirname(self._config_file), secrets_path)

    def load_secrets(self) -> Any:
        """Lade die Secrets-Datei und gebe den Inhalt zurück."""
        if not os.path.exists(self._secrets_file_path):
            raise FileNotFoundError(f"Die Datei {self._secrets_file_path} wurde nicht gefunden.")

        with open(self._secrets_file_path, "r") as f:
            secrets = json.load(f)
        return secrets

    def return_secret(self, key: str) -> Any:
        """Gibt das Secret für den angegebenen Schlüssel zurück."""
        return self._secrets.get(key)
    # endregion
