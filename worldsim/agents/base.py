"""Provider-neutral agent contract."""
from abc import ABC, abstractmethod
from worldsim.models import CountryState, PolicyDecision


class CountryAgent(ABC):
    @abstractmethod
    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        """Return one structured policy decision for the next year."""
        raise NotImplementedError
