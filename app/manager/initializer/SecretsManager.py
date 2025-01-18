import threading
from typing import Any
from app.GlobalVariables import ENV
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
    def __init__(self, config_file='/Users/lauris/PycharmProjects/AutomatedTrading/app/config.ini'):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._config_file = config_file
            self._secrets_file_path = self.load_secrets_path()
            # print(f"Pfad zur Secrets-Datei: {self.secrets_file_path}")  # Debug-Ausgabe
            self._secrets = self.load_secrets()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Secrets Functions
    def load_secrets_path(self)-> Any:
        """Lade den Pfad zur Secrets-Datei aus der Konfigurationsdatei."""
        import os
        from configparser import ConfigParser
        environment_path = "secrets_path"
        environment_path = environment_path.replace("secrets",ENV).upper()
        config = ConfigParser()
        config.read(self._config_file)
        secretsPath = config.get('paths', environment_path, fallback='config/secrets.json')
        # print(f"Gelegter secrets_path: {secrets_path}")  # Debug-Ausgabe
        return os.path.join(os.path.dirname(self._config_file), secretsPath)

    def load_secrets(self) -> Any:
        """Lade die Secrets-Datei und gebe den Inhalt zurück."""
        import json
        import os
        if not os.path.exists(self._secrets_file_path):
            raise FileNotFoundError(f"Die Datei {self._secrets_file_path} wurde nicht gefunden.")
        with open(self._secrets_file_path, 'r') as f:
            secrets = json.load(f)
        return secrets

    def return_secret(self, key) -> Any:
        """Gibt das Secret für den angegebenen Schlüssel zurück."""
        return self._secrets.get(key)
    # endregion
