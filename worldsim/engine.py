"""Deterministic simulation rules. AI never directly edits country state."""
from copy import deepcopy
from worldsim.models import CountryState, PolicyDecision, YearRecord


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class SimulationEngine:
    def advance(self, state: CountryState, decision: PolicyDecision) -> YearRecord:
        if decision.country_code != state.code:
            raise ValueError("Decision country_code does not match state.")
        if decision.year != state.year + 1:
            raise ValueError("Decision year must be exactly the next simulation year.")

        next_state = deepcopy(state)
        # Small, transparent teaching coefficients; not an econometric forecast.
        growth = 1.2 + 0.45 * decision.economy
        growth += 0.025 * (next_state.education - 50)
        growth += 0.02 * (next_state.infrastructure - 50)
        growth -= max(0, next_state.inflation - 6) * 0.08

        next_state.gdp_index = max(1, next_state.gdp_index * (1 + growth / 100))
        next_state.inflation = _clamp(
            next_state.inflation + 0.25 * decision.economy - 0.12 * decision.infrastructure,
            0, 100,
        )
        next_state.unemployment = _clamp(
            next_state.unemployment - 0.18 * decision.economy - 0.08 * decision.infrastructure,
            0, 100,
        )
        next_state.education = _clamp(next_state.education + 0.35 * decision.education, 0, 100)
        next_state.infrastructure = _clamp(
            next_state.infrastructure + 0.35 * decision.infrastructure, 0, 100
        )
        next_state.defense = _clamp(next_state.defense + 0.4 * decision.defense, 0, 100)
        next_state.treasury = _clamp(
            next_state.treasury - 0.35 * sum(abs(getattr(decision, key)) for key in
                ("economy", "education", "infrastructure", "defense")),
            0, 100,
        )
        approval_delta = (
            0.12 * (growth - 1.2)
            - 0.08 * (next_state.inflation - state.inflation)
            - 0.08 * (next_state.unemployment - state.unemployment)
        )
        next_state.approval = _clamp(next_state.approval + approval_delta, 0, 100)
        next_state.year = decision.year

        return YearRecord(
            year=next_state.year,
            country_code=next_state.code,
            decision=decision,
            state=next_state,
        )
