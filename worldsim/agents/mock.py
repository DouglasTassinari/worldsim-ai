"""Deterministic demo agent; no external API calls or costs."""
from worldsim.agents.base import CountryAgent
from worldsim.models import CountryState, PolicyDecision


class MockAgent(CountryAgent):
    def __init__(self, style: str = "balanced"):
        self.style = style

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        if self.style == "growth":
            values = dict(economy=2, education=1, infrastructure=1, defense=0, diplomacy=1)
            rationale = "Prioriza crescimento, capital humano e infraestrutura."
        elif self.style == "security":
            values = dict(economy=0, education=0, infrastructure=0, defense=2, diplomacy=-1)
            rationale = "Prioriza segurança e capacidade de defesa."
        else:
            values = dict(economy=1, education=1, infrastructure=1, defense=0, diplomacy=1)
            rationale = "Busca equilíbrio entre crescimento e estabilidade."
        return PolicyDecision(
            country_code=state.code,
            year=state.year + 1,
            priorities=[],
            rationale=rationale,
            **values,
        )
