"""OpenAI-backed governor. Different countries share a model but receive distinct worldviews."""
import os
from worldsim.agents.base import CountryAgent
from worldsim.agents.prompting import build_country_prompt, parse_decision
from worldsim.agents.profiles import IdeologyProfile, get_profile
from worldsim.models import CountryState, PolicyDecision


class OpenAIAgent(CountryAgent):
    def __init__(self, model: str = "gpt-4.1-mini", profile: IdeologyProfile | None = None):
        self.model = model
        self.profile = profile or get_profile("social_liberal")

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.responses.create(model=self.model, input=build_country_prompt(state, world_context, self.profile))
        return parse_decision(response.output_text, state)
