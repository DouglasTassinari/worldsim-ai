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
