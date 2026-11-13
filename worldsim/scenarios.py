"""Illustrative scenario presets. Values are normalized starting conditions, not official statistics."""
from worldsim.models import CountryState, BilateralRelation, WorldState


def south_america_2026(seed: int = 42) -> WorldState:
    brazil = CountryState(name="Brasil", code="BRA", year=2026, gdp_index=100, population_m=212,
        inflation=4.5, unemployment=7.5, approval=52, education=55, infrastructure=48,
        health=58, defense=58, productivity=55, institutions=62, inequality=52,
        stability=72, debt_gdp=78, fiscal_balance=-2.5, trade_balance=1.0,
        exchange_rate_index=100, treasury=55)
    argentina = CountryState(name="Argentina", code="ARG", year=2026, gdp_index=35, population_m=46,
        inflation=25, unemployment=7.5, approval=48, education=58, infrastructure=48,
        health=62, defense=42, productivity=50, institutions=48, inequality=42,
        stability=52, debt_gdp=85, fiscal_balance=-3.0, trade_balance=0.5,
        exchange_rate_index=100, treasury=32)
    return WorldState(year=2026, seed=seed, countries={"BRA": brazil, "ARG": argentina},
        relations=[BilateralRelation(country_a="BRA", country_b="ARG", score=62, tariff_pct=8, trade_volume=12)])


def demo_world(seed: int = 42) -> WorldState:
    return south_america_2026(seed)
