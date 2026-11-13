"""Deterministic sample policies; useful for demos and tests without API costs."""
from worldsim.agents.base import CountryAgent
from worldsim.models import CountryState, PolicyDecision


class MockAgent(CountryAgent):
    def __init__(self, style: str = "balanced"):
        self.style = style

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        common = dict(country_code=state.code, year=state.year + 1)
        if self.style == "growth":
            return PolicyDecision(**common, tax_change=-1, monetary_tightening=0,
                education_budget=16, infrastructure_budget=18, health_budget=12,
                defense_budget=6, institutions_budget=6, trade_openness=1, diplomacy=1,
                rationale="Agenda de crescimento com investimento em capital humano e infraestrutura.")
        if self.style == "austerity":
            return PolicyDecision(**common, tax_change=1, monetary_tightening=1,
                education_budget=10, infrastructure_budget=8, health_budget=9,
                defense_budget=7, institutions_budget=5, trade_openness=0, diplomacy=0,
                rationale="Consolidação fiscal gradual, com custo potencial de crescimento no curto prazo.")
        tax_change = 1 if state.inflation > 15 else 0
        monetary = 2 if state.inflation > 20 else (1 if state.inflation > 8 else 0)
        return PolicyDecision(**common, tax_change=tax_change, monetary_tightening=monetary,
            education_budget=13, infrastructure_budget=12, health_budget=12,
            defense_budget=8, institutions_budget=6, trade_openness=1, diplomacy=1,
            rationale="Estratégia equilibrada, com aperto fiscal e monetário adicional quando a inflação está muito acima da meta.")
