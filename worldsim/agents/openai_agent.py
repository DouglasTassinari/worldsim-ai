"""Optional OpenAI adapter. Install the openai extra and set OPENAI_API_KEY."""
import os
from worldsim.agents.base import CountryAgent
from worldsim.agents.prompting import build_country_prompt, parse_decision
from worldsim.models import CountryState, PolicyDecision


class OpenAIAgent(CountryAgent):
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.responses.create(model=self.model, input=build_country_prompt(state, world_context))
        return parse_decision(response.output_text, state)
