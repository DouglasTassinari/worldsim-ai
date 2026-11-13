"""Optional Anthropic adapter. Install the anthropic extra and set ANTHROPIC_API_KEY."""
import os
from worldsim.agents.base import CountryAgent
from worldsim.agents.prompting import build_country_prompt, parse_decision
from worldsim.models import CountryState, PolicyDecision


class AnthropicAgent(CountryAgent):
    def __init__(self, model: str = "claude-sonnet-4-5"):
        self.model = model

    def decide(self, state: CountryState, world_context: str = "") -> PolicyDecision:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        message = client.messages.create(model=self.model, max_tokens=1200,
            messages=[{"role": "user", "content": build_country_prompt(state, world_context)}])
        text = next(block.text for block in message.content if block.type == "text")
        return parse_decision(text, state)
