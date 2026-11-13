"""Optional Google Gemini adapter. Install google-genai extra and set GOOGLE_API_KEY."""
import os
from worldsim.agents.base import CountryAgent
from worldsim.agents.prompting import build_country_prompt, parse_decision
from worldsim.models import CountryState, PolicyDecision


class GoogleAgent(CountryAgent):
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        from google import genai
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        response = client.models.generate_content(model=self.model,
            contents=build_country_prompt(state, world_context))
        return parse_decision(response.text or "", state)
