"""Typed domain models for the simulation."""
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class PolicyArea(str, Enum):
    ECONOMY = "economy"
    EDUCATION = "education"
    INFRASTRUCTURE = "infrastructure"
    DEFENSE = "defense"
    DIPLOMACY = "diplomacy"


class CountryState(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    name: str
    code: str
    year: int = 2026
    gdp_index: float = Field(default=100.0, ge=1)
    inflation: float = Field(default=4.0, ge=0, le=100)
    unemployment: float = Field(default=8.0, ge=0, le=100)
    approval: float = Field(default=50.0, ge=0, le=100)
    education: float = Field(default=50.0, ge=0, le=100)
    infrastructure: float = Field(default=50.0, ge=0, le=100)
    defense: float = Field(default=50.0, ge=0, le=100)
    treasury: float = Field(default=50.0, ge=0, le=100)


class PolicyDecision(BaseModel):
    """Agent output. Values are bounded before the engine applies them."""

    country_code: str
    year: int
    priorities: list[PolicyArea] = Field(default_factory=list, max_length=3)
    economy: int = Field(default=0, ge=-2, le=2)
    education: int = Field(default=0, ge=-2, le=2)
    infrastructure: int = Field(default=0, ge=-2, le=2)
    defense: int = Field(default=0, ge=-2, le=2)
    diplomacy: int = Field(default=0, ge=-2, le=2)
    rationale: str = Field(default="", max_length=500)


class YearRecord(BaseModel):
    year: int
    country_code: str
    decision: PolicyDecision
    state: CountryState
    events: list[str] = Field(default_factory=list)
