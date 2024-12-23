import threading
from typing import Any

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
    def __init__(self, configFile='/Users/lauris/PycharmProjects/AutomatedTrading/config/config.ini'):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert

            self._configFile = configFile
            self._secretsFilePath = self.loadSecretsPath()
            # print(f"Pfad zur Secrets-Datei: {self.secrets_file_path}")  # Debug-Ausgabe
            self._secrets = self.loadSecrets()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Secrets Functions
    def loadSecretsPath(self)-> Any:
        """Lade den Pfad zur Secrets-Datei aus der Konfigurationsdatei."""
        import os
        from configparser import ConfigParser
        config = ConfigParser()
        config.read(self._configFile)
        secretsPath = config.get('paths', 'secrets_path', fallback='config/secrets.json')
        # print(f"Gelegter secrets_path: {secrets_path}")  # Debug-Ausgabe
        return os.path.join(os.path.dirname(self._configFile), secretsPath)

    def loadSecrets(self) -> Any:
        """Lade die Secrets-Datei und gebe den Inhalt zurück."""
        import json
        import os
        if not os.path.exists(self._secretsFilePath):
            raise FileNotFoundError(f"Die Datei {self._secretsFilePath} wurde nicht gefunden.")
        with open(self._secretsFilePath, 'r') as f:
            secrets = json.load(f)
        return secrets

    def returnSecret(self, key) -> Any:
        """Gibt das Secret für den angegebenen Schlüssel zurück."""
        return self._secrets.get(key)
    # endregion
