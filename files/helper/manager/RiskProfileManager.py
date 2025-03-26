import threading
from logging import Logger

from files.helper.calculator.RiskProfileAnalyzer import RiskProfileAnalyzer
from files.models.asset.Relation import Relation
from files.models.risk.RiskProfile import RiskProfile

from files.models.risk.RiskProfileInput import RiskProfileInput
#todo class instance

# todo Hybrid-Ansatz mit Lazy Loading
#
# Halte häufig genutzte Daten im Speicher.
# Lade selten genutzte Daten on demand aus der Datenbank.

class RiskProfileManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RiskProfileManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,logger:Logger,risk_profile_analyzer:RiskProfileAnalyzer):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._risk_profiles:dict[str,RiskProfile] = {}
            self._risk_profile_analyzer = risk_profile_analyzer
            self._logger = logger
            self._initialized = True

    def add_profile(self, relation: Relation, risk_profile: RiskProfile):
        if relation.asset + relation.broker not in self._risk_profiles:
            self._risk_profiles[relation.asset + relation.broker] = risk_profile
            self._logger.info(f"Risk Profile for {relation.asset} + {relation.broker} registered")

    def delete_mediator(self, relation: Relation):
        try:
            if relation.asset + relation.broker in self._risk_profiles:
                del self._risk_profiles[relation.asset + relation.broker]
                self._logger.info(f"Risk Profile for {relation.asset} + {relation.broker} deleted")
        except Exception as e:
            self._logger.exception(f"Risk Profile for {relation.asset} + {relation.broker} deletion failed: {e}")

    def get_risk_profile(self, relation: Relation) -> RiskProfile:
        try:
            if relation.asset + relation.broker in self._risk_profiles:
                return self._risk_profiles[relation.asset + relation.broker]
        except Exception as e:
            self._logger.exception(f"{relation.asset} + {relation.broker} retrieval failed: {e}")

    def update_risk_profile(self, relation: Relation, risk_profile_inputs: RiskProfileInput):
        try:
            if relation.asset + relation.broker in self._risk_profiles:
                risk_profile = self._risk_profiles[relation.asset + relation.broker]
                self._risk_profiles[relation.asset + relation.broker] = self._risk_profile_analyzer.update_risk_profile(risk_profile, risk_profile_inputs)
        except Exception as e:
            self._logger.exception(f"Risk Profile: {relation.asset} + {relation.broker} update failed: {e}")