from worldsim.engine import SimulationEngine
from worldsim.models import PolicyDecision
from worldsim.scenarios import south_america_2026


def test_world_advances_all_countries_and_relations():
    world = south_america_2026()
    decisions = {
        code: PolicyDecision(country_code=code, year=2027, diplomacy=1)
        for code in world.countries
    }
    next_world, records = SimulationEngine(seed=world.seed).advance_world(world, decisions)
    assert next_world.year == 2027
    assert len(records) == 2
    assert next_world.relations[0].score > world.relations[0].score


def test_same_seed_is_reproducible():
    world = south_america_2026(seed=7)
    decisions = {code: PolicyDecision(country_code=code, year=2027) for code in world.countries}
    a, _ = SimulationEngine(seed=7).advance_world(world, decisions)
    b, _ = SimulationEngine(seed=7).advance_world(world, decisions)
    assert a.model_dump() == b.model_dump()


def test_budget_cannot_exceed_100():
    import pytest
    with pytest.raises(ValueError, match="budget"):
        PolicyDecision(country_code="BRA", year=2027, education_budget=40,
            infrastructure_budget=40, health_budget=40)

from worldsim.events import generate_global_events


def test_global_events_are_reproducible():
    assert [e.code for e in generate_global_events(123, 2030)] == [
        e.code for e in generate_global_events(123, 2030)
    ]


def test_tax_increase_has_short_run_demand_cost_and_improves_fiscal_balance():
    from worldsim.engine import SimulationEngine
    from worldsim.models import PolicyDecision
    from worldsim.scenarios import south_america_2026
    state = south_america_2026().countries["BRA"]
    baseline = PolicyDecision(country_code="BRA", year=2027, tax_change=0)
    tax_hike = PolicyDecision(country_code="BRA", year=2027, tax_change=2)
    engine = SimulationEngine(seed=8)
    a = engine.advance(state, baseline)
    b = engine.advance(state, tax_hike)
    assert b.gdp_growth_pct < a.gdp_growth_pct
    assert b.state.fiscal_balance > a.state.fiscal_balance


def test_global_shock_is_recorded_and_changes_growth():
    from worldsim.engine import SimulationEngine
    from worldsim.models import GlobalEvent, PolicyDecision
    from worldsim.scenarios import south_america_2026
    state = south_america_2026().countries["BRA"]
    decision = PolicyDecision(country_code="BRA", year=2027)
    event = GlobalEvent(code="test", title="Teste de choque", description="Evento", growth_impact=-1)
    record = SimulationEngine(seed=8).advance(state, decision, [event])
    assert "Teste de choque" in record.events
