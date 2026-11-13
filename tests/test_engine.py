import pytest
from worldsim.agents.mock import MockAgent
from worldsim.engine import SimulationEngine
from worldsim.models import CountryState


def sample_state():
    return CountryState(name="Brasil", code="BRA", year=2026)


def test_engine_advances_exactly_one_year():
    state = sample_state()
    decision = MockAgent().decide(state)
    record = SimulationEngine().advance(state, decision)
    assert record.state.year == 2027
    assert state.year == 2026  # original state is not mutated


def test_engine_rejects_wrong_country():
    state = sample_state()
    decision = MockAgent().decide(state).model_copy(update={"country_code": "ARG"})
    with pytest.raises(ValueError, match="country_code"):
        SimulationEngine().advance(state, decision)


def test_engine_rejects_wrong_year():
    state = sample_state()
    decision = MockAgent().decide(state).model_copy(update={"year": 2030})
    with pytest.raises(ValueError, match="year"):
        SimulationEngine().advance(state, decision)


def test_indicators_remain_in_valid_ranges():
    state = sample_state()
    record = SimulationEngine().advance(state, MockAgent("growth").decide(state))
    for field in ("inflation", "unemployment", "approval", "education",
                  "infrastructure", "defense", "treasury"):
        assert 0 <= getattr(record.state, field) <= 100
