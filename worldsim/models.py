"""Validated domain models. All numeric indicators are simulation units, not official forecasts."""
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, model_validator


class PolicyArea(str, Enum):
    TAX = "tax"
    MONETARY = "monetary"
    EDUCATION = "education"
    INFRASTRUCTURE = "infrastructure"
    HEALTH = "health"
    DEFENSE = "defense"
    TRADE = "trade"
    INSTITUTIONS = "institutions"


class CountryState(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str
    code: str
    year: int = 2026
    gdp_index: float = Field(default=100, gt=0)
    population_m: float = Field(default=50, gt=0)
    population_growth_pct: float = Field(default=0.5, ge=-5, le=5)
    potential_growth: float = Field(default=2.0, ge=-10, le=15)
    inflation: float = Field(default=4, ge=0, le=300)
    unemployment: float = Field(default=7, ge=0, le=100)
    approval: float = Field(default=50, ge=0, le=100)
    education: float = Field(default=50, ge=0, le=100)
    infrastructure: float = Field(default=50, ge=0, le=100)
    health: float = Field(default=50, ge=0, le=100)
    defense: float = Field(default=50, ge=0, le=100)
    productivity: float = Field(default=50, ge=0, le=100)
    institutions: float = Field(default=50, ge=0, le=100)
    inequality: float = Field(default=50, ge=0, le=100)
    stability: float = Field(default=65, ge=0, le=100)
    debt_gdp: float = Field(default=60, ge=0, le=500)
    fiscal_balance: float = Field(default=-2, ge=-30, le=30)
    trade_balance: float = Field(default=0, ge=-30, le=30)
    exchange_rate_index: float = Field(default=100, gt=0)
    treasury: float = Field(default=50, ge=0, le=100)


class PolicyDecision(BaseModel):
    """Government proposal. Budget shares must total 100; engine applies bounded effects."""
    country_code: str
    year: int
    tax_change: int = Field(default=0, ge=-2, le=2)
    monetary_tightening: int = Field(default=0, ge=-2, le=2)
    education_budget: int = Field(default=12, ge=0, le=40)
    infrastructure_budget: int = Field(default=12, ge=0, le=40)
    health_budget: int = Field(default=10, ge=0, le=40)
    defense_budget: int = Field(default=8, ge=0, le=40)
    institutions_budget: int = Field(default=5, ge=0, le=25)
    trade_openness: int = Field(default=0, ge=-2, le=2)
    diplomacy: int = Field(default=0, ge=-2, le=2)
    rationale: str = Field(default="", max_length=700)

    @model_validator(mode="after")
    def validate_budget(self):
        total = self.education_budget + self.infrastructure_budget + self.health_budget + self.defense_budget + self.institutions_budget
        if total > 100:
            raise ValueError("Total policy budget shares cannot exceed 100.")
        return self


class BilateralRelation(BaseModel):
    country_a: str
    country_b: str
    score: float = Field(default=50, ge=0, le=100)
    tariff_pct: float = Field(default=5, ge=0, le=100)
    trade_volume: float = Field(default=10, ge=0)


class GlobalEvent(BaseModel):
    code: str
    title: str
    description: str
    growth_impact: float = 0
    inflation_impact: float = 0
    trade_impact: float = 0


class WorldState(BaseModel):
    year: int = 2026
    countries: dict[str, CountryState]
    relations: list[BilateralRelation] = Field(default_factory=list)
    seed: int = 42


class YearRecord(BaseModel):
    year: int
    country_code: str
    decision: PolicyDecision
    state: CountryState
    events: list[str] = Field(default_factory=list)
    gdp_growth_pct: float = 0
