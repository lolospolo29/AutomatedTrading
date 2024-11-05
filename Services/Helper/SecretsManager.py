import json
import os
from configparser import ConfigParser
from typing import Any


class SecretsManager:
    def __init__(self, configFile='C:\\AutomatedTrading\\Config\\config.ini'):
        self.configFile = configFile
        self.secretsFilePath = self.loadSecretsPath()
        # print(f"Pfad zur Secrets-Datei: {self.secrets_file_path}")  # Debug-Ausgabe
        self.secrets = self.loadSecrets()

    def loadSecretsPath(self)-> Any:
        """Lade den Pfad zur Secrets-Datei aus der Konfigurationsdatei."""
        config = ConfigParser()
        config.read(self.configFile)
        secretsPath = config.get('paths', 'secrets_path', fallback='Config/secrets.json')
        # print(f"Gelegter secrets_path: {secrets_path}")  # Debug-Ausgabe
        return os.path.join(os.path.dirname(self.configFile), secretsPath)

    def loadSecrets(self) -> Any:
        """Lade die Secrets-Datei und gebe den Inhalt zurück."""
        if not os.path.exists(self.secretsFilePath):
            raise FileNotFoundError(f"Die Datei {self.secretsFilePath} wurde nicht gefunden.")
        with open(self.secretsFilePath, 'r') as f:
            secrets = json.load(f)
        return secrets

    def returnSecret(self, key) -> Any:
        """Gibt das Secret für den angegebenen Schlüssel zurück."""
        return self.secrets.get(key)
