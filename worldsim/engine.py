"""Transparent, deterministic rules-based macro simulation (stylized, not a forecast)."""
from copy import deepcopy
import random
from worldsim.models import CountryState, PolicyDecision, YearRecord, WorldState, GlobalEvent
from worldsim.events import generate_global_events


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


class SimulationEngine:
    def __init__(self, seed: int = 42):
        self.seed = seed

    def advance(self, state: CountryState, decision: PolicyDecision, global_events: list[GlobalEvent] | None = None) -> YearRecord:
        if decision.country_code != state.code:
            raise ValueError("Decision country_code does not match state.")
        if decision.year != state.year + 1:
            raise ValueError("Decision year must be exactly the next simulation year.")

        s = deepcopy(state)
        rng = random.Random(f"{self.seed}:{state.code}:{decision.year}")
        events: list[str] = [event.title for event in (global_events or [])]
        old = state

        # Budget allocations are shares of a stylized public budget.
        education_impulse = (decision.education_budget - 12) / 10
        infrastructure_impulse = (decision.infrastructure_budget - 12) / 10
        health_impulse = (decision.health_budget - 10) / 10
        defense_impulse = (decision.defense_budget - 8) / 10
        institution_impulse = (decision.institutions_budget - 5) / 5

        # Demand, supply, productivity and external conditions.
        demand = -0.25 * decision.tax_change - 0.38 * decision.monetary_tightening
        public_investment = 0.10 * infrastructure_impulse
        human_capital = 0.045 * (s.education - 50) / 10 + 0.035 * education_impulse
        productivity = 0.035 * (s.productivity - 50) / 10
        institutions = 0.025 * (s.institutions - 50) / 10 + 0.025 * institution_impulse
        inflation_drag = max(0, s.inflation - 4.0) * 0.055
        unemployment_gap = (7.0 - s.unemployment) * 0.035
        shock = rng.uniform(-0.65, 0.65)
        global_events = global_events or []
        event_growth = sum(event.growth_impact for event in global_events)
        event_inflation = sum(event.inflation_impact for event in global_events)
        event_trade = sum(event.trade_impact for event in global_events)
        growth = s.potential_growth + demand + public_investment + human_capital + productivity + institutions + unemployment_gap - inflation_drag + shock + event_growth

        # Monetary policy influences inflation with a lag and has a short-run output cost.
        inflation_pressure = 0.16 * (growth - s.potential_growth) - 0.10 * decision.tax_change
        inflation_pressure -= 0.42 * decision.monetary_tightening
        inflation_pressure += rng.uniform(-0.25, 0.25) + event_inflation
        s.inflation = clamp(s.inflation + inflation_pressure, 0.2, 250)

        # Employment responds to growth, investment and the inflation/interest trade-off.
        s.unemployment = clamp(s.unemployment - 0.16 * (growth - 1.5) + 0.10 * decision.monetary_tightening, 2, 35)

        # Long-term stocks move slowly; investment is not instantly productive.
        s.education = clamp(s.education + 0.10 * education_impulse + 0.018 * (s.health - 50) / 10, 0, 100)
        s.infrastructure = clamp(s.infrastructure + 0.12 * infrastructure_impulse, 0, 100)
        s.health = clamp(s.health + 0.10 * health_impulse, 0, 100)
        s.defense = clamp(s.defense + 0.10 * defense_impulse, 0, 100)
        s.institutions = clamp(s.institutions + 0.08 * institution_impulse, 0, 100)
        s.productivity = clamp(s.productivity + 0.025 * (s.education - 50) / 10 + 0.02 * (s.infrastructure - 50) / 10 + 0.015 * (s.institutions - 50) / 10, 0, 100)

        # Fiscal balance, debt dynamics and fiscal space.
        spending = (decision.education_budget + decision.infrastructure_budget + decision.health_budget + decision.defense_budget + decision.institutions_budget)
        fiscal_change = 0.20 * decision.tax_change - 0.025 * (spending - 47) - 0.08 * infrastructure_impulse
        s.fiscal_balance = clamp(s.fiscal_balance + fiscal_change, -20, 15)
        nominal_growth = growth + s.inflation
        s.debt_gdp = clamp(s.debt_gdp - s.fiscal_balance + 0.012 * s.debt_gdp * max(0, 3 - nominal_growth), 0, 300)
        s.treasury = clamp(s.treasury - max(0, -s.fiscal_balance - 2) * 0.12 + max(0, s.fiscal_balance) * 0.08, 0, 100)

        # External competitiveness and exchange rate pressure.
        s.trade_balance = clamp(s.trade_balance + 0.12 * decision.trade_openness - 0.04 * (growth - 2) + event_trade, -20, 20)
        fx_pressure = 0.12 * (s.inflation - 4) - 0.10 * s.trade_balance - 0.08 * decision.monetary_tightening
        s.exchange_rate_index = max(5, s.exchange_rate_index * (1 + fx_pressure / 100))

        # Social outcomes and political legitimacy.
        s.inequality = clamp(s.inequality - 0.025 * health_impulse - 0.025 * education_impulse + 0.02 * max(0, -s.fiscal_balance - 5), 0, 100)
        s.population_m = max(0.1, s.population_m * (1 + s.population_growth_pct / 100))
        s.stability = clamp(s.stability + 0.04 * (s.approval - 50) - 0.10 * max(0, s.inflation - 8) - 0.10 * max(0, s.unemployment - 10) + 0.04 * institution_impulse, 0, 100)
        approval_delta = 0.10 * (growth - 2) - 0.08 * (s.inflation - old.inflation) - 0.12 * (s.unemployment - old.unemployment) + 0.025 * (s.health - old.health) - 0.025 * (s.inequality - old.inequality)
        s.approval = clamp(s.approval + approval_delta, 0, 100)
        s.gdp_index = max(1, s.gdp_index * (1 + growth / 100))
        s.year = decision.year

        if growth < -1:
            events.append("Recessão: a atividade econômica contraiu.")
        if s.inflation > 10:
            events.append("Inflação elevada pressiona renda e estabilidade.")
        if s.debt_gdp > 100:
            events.append("Dívida pública acima de 100% do PIB reduz espaço fiscal.")
        if s.approval < 25:
            events.append("Crise de popularidade: risco político elevado.")
        if s.stability < 30:
            events.append("Instabilidade institucional severa.")
        if not events:
            events.append("Ano sem evento crítico automático.")

        return YearRecord(year=s.year, country_code=s.code, decision=decision, state=s, events=events, gdp_growth_pct=growth)

    def advance_world(self, world: WorldState, decisions: dict[str, PolicyDecision]) -> tuple[WorldState, list[YearRecord]]:
        """Advance every country once, then update bilateral relations."""
        next_world = deepcopy(world)
        records = []
        global_events = generate_global_events(world.seed, world.year + 1)
        for code, state in world.countries.items():
            if code not in decisions:
                raise ValueError(f"Missing decision for {code}")
            record = self.advance(state, decisions[code], global_events)
            next_world.countries[code] = record.state
            records.append(record)
        for relation in next_world.relations:
            da = decisions[relation.country_a].diplomacy
            db = decisions[relation.country_b].diplomacy
            relation.score = clamp(relation.score + 1.4 * (da + db) - 0.8 * abs(da - db), 0, 100)
            relation.tariff_pct = clamp(relation.tariff_pct - 0.35 * (da + db), 0, 60)
            relation.trade_volume = max(0, relation.trade_volume * (1 + (relation.score - 50) / 1000 - relation.tariff_pct / 2000))
        next_world.year += 1
        return next_world, records
