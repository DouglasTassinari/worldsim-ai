"""Reproducible global shocks. Event probabilities and impacts are gameplay assumptions."""
import random
from worldsim.models import GlobalEvent

EVENTS = [
    (0.045, GlobalEvent(code="global_slowdown", title="Desaceleração global", description="A demanda internacional enfraquece.", growth_impact=-0.9, inflation_impact=-0.1, trade_impact=-0.3)),
    (0.025, GlobalEvent(code="energy_supply_shock", title="Choque de oferta energética", description="Energia e transporte ficam mais caros.", growth_impact=-0.45, inflation_impact=1.0, trade_impact=-0.25)),
    (0.018, GlobalEvent(code="financial_stress", title="Estresse financeiro internacional", description="Condições de crédito globais se apertam.", growth_impact=-1.2, inflation_impact=0.35, trade_impact=-0.4)),
    (0.012, GlobalEvent(code="pandemic", title="Emergência sanitária internacional", description="Uma crise sanitária afeta produção, mobilidade e serviços.", growth_impact=-2.0, inflation_impact=0.6, trade_impact=-0.8)),
    (0.035, GlobalEvent(code="productivity_wave", title="Onda de ganhos de produtividade", description="Uma difusão tecnológica melhora a produtividade global.", growth_impact=0.55, inflation_impact=-0.15, trade_impact=0.15)),
    (0.025, GlobalEvent(code="climate_disruption", title="Evento climático extremo", description="Eventos climáticos afetam safras, infraestrutura e logística.", growth_impact=-0.6, inflation_impact=0.55, trade_impact=-0.2)),
]


def generate_global_events(seed: int, year: int) -> list[GlobalEvent]:
    rng = random.Random(f"world-events:{seed}:{year}")
    return [event.model_copy(deep=True) for probability, event in EVENTS if rng.random() < probability]
