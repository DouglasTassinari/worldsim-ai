"""Illustrative scenario presets seeded from IMF WEO October 2026 projections."""
from worldsim.models import CountryState, BilateralRelation, WorldState


def south_america_2026(seed: int = 42) -> WorldState:
    # Macro baseline uses IMF WEO October 2026 estimates/projections.
    # GDP index is normalized: Brazil=100; Argentina is relative to nominal USD GDP.
    brazil = CountryState(name="Brasil", code="BRA", year=2026, gdp_index=100,
        population_m=214.14, population_growth_pct=0.4, potential_growth=2.2,
        inflation=4.4, unemployment=6.2, approval=50, education=55,
        infrastructure=50, health=60, defense=55, productivity=55,
        institutions=62, inequality=52, stability=70, debt_gdp=97,
        fiscal_balance=-8.1, trade_balance=-2.4, exchange_rate_index=100, treasury=45)
    argentina = CountryState(name="Argentina", code="ARG", year=2026, gdp_index=29,
        population_m=47.95, population_growth_pct=0.3, potential_growth=2.1,
        inflation=32.5, unemployment=7.6, approval=50, education=58,
        infrastructure=48, health=62, defense=42, productivity=50,
        institutions=48, inequality=42, stability=52, debt_gdp=69.3,
        fiscal_balance=0.4, trade_balance=0.6, exchange_rate_index=100, treasury=48)
    return WorldState(year=2026, seed=seed, countries={"BRA": brazil, "ARG": argentina},
        relations=[BilateralRelation(country_a="BRA", country_b="ARG", score=62, tariff_pct=8, trade_volume=12)])


def demo_world(seed: int = 42) -> WorldState:
    return south_america_2026(seed)
