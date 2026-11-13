"""Single-provider agent factory: every live governor uses the same OpenAI model."""
from worldsim.agents.openai_agent import OpenAIAgent
from worldsim.agents.mock import MockAgent
from worldsim.agents.profiles import get_profile


def build_agent(profile_id: str, *, demo: bool = False, model: str = "gpt-4.1-mini"):
    profile = get_profile(profile_id)
    if demo:
        # Deterministic local stand-in for interface/testing; not an AI provider.
        style_by_profile = {
            "social_liberal": "balanced", "market_liberal": "growth",
            "nationalist": "austerity", "socialist": "balanced",
            "authoritarian": "austerity", "green": "balanced",
        }
        return MockAgent(style_by_profile[profile_id])
    return OpenAIAgent(model=model, profile=profile)
