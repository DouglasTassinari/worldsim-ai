"""Run comparable experiments from identical starting conditions."""
from copy import deepcopy
from worldsim.engine import SimulationEngine
from worldsim.agents.factory import build_agent


def run_experiment(initial_world, assignments: dict[str, str], years: int,
                   *, demo: bool = False, model: str = "gpt-4.1-mini"):
    unknown = set(assignments) - set(initial_world.countries)
    missing = set(initial_world.countries) - set(assignments)
    if unknown or missing:
        raise ValueError(f"Assignments must cover every country. Missing={sorted(missing)}, unknown={sorted(unknown)}")
    world = deepcopy(initial_world)
    engine = SimulationEngine(seed=world.seed)
    history = []
    agents = {code: build_agent(profile_id, demo=demo, model=model)
              for code, profile_id in assignments.items()}
    for _ in range(years):
        decisions = {}
        for code, state in world.countries.items():
            context = "Relações bilaterais: " + "; ".join(
                f"{r.country_a}-{r.country_b}: relação {r.score:.0f}/100, tarifa {r.tariff_pct:.1f}%"
                for r in world.relations
            )
            decisions[code] = agents[code].decide(state, context)
        world, records = engine.advance_world(world, decisions)
        history.extend(records)
    return world, history
