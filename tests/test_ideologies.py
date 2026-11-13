from worldsim.agents.profiles import PROFILES, get_profile
from worldsim.experiments import run_experiment
from worldsim.scenarios import south_america_2026


def test_profiles_are_distinct_and_country_independent():
    assert len(PROFILES) >= 6
    assert len({p.priorities for p in PROFILES.values()}) == len(PROFILES)
    assert get_profile("market_liberal").id == "market_liberal"


def test_experiment_assignments_cover_all_countries():
    world = south_america_2026()
    try:
        run_experiment(world, {"BRA": "social_liberal"}, 1, demo=True)
    except ValueError as exc:
        assert "cover every country" in str(exc)
    else:
        raise AssertionError("Incomplete assignment should fail")


def test_same_seed_and_assignment_are_reproducible_in_demo():
    world = south_america_2026(seed=17)
    assignment = {"BRA": "market_liberal", "ARG": "socialist"}
    a, _ = run_experiment(world, assignment, 2, demo=True)
    b, _ = run_experiment(world, assignment, 2, demo=True)
    assert a.model_dump() == b.model_dump()
