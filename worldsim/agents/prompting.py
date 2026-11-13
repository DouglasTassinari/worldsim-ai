"""Prompt construction and strict parsing helpers for LLM country agents."""
import json
from worldsim.agents.profiles import IdeologyProfile
from worldsim.models import CountryState, PolicyDecision


def build_country_prompt(state: CountryState, world_context: str = "", profile: IdeologyProfile | None = None) -> str:
    schema = json.dumps(PolicyDecision.model_json_schema(), ensure_ascii=False)
    worldview = ""
    if profile:
        worldview = f"""
PERFIL DO GOVERNANTE: {profile.name}
Visão de mundo: {profile.description}
Prioridades: {profile.priorities}
Trade-offs aceitos: {profile.tradeoffs}
Política externa: {profile.foreign_policy}
Aplique esse conjunto de valores de forma consistente, sem caricaturas. Considere as condições reais do país, restrições institucionais, orçamento e efeitos colaterais.
"""
    return f"""Você é o chefe de governo de {state.name} em uma simulação estratégica.
{worldview}
Ano atual: {state.year}. Estado oficial do jogo:
{json.dumps(state.model_dump(), ensure_ascii=False)}
Contexto internacional:
{world_context or "Sem informação adicional."}

Produza UMA decisão anual em JSON, obedecendo ao schema fornecido.
Não invente resultados nem altere indicadores diretamente. Escolha políticas com trade-offs:
- impostos e aperto monetário afetam demanda, inflação e contas públicas;
- educação, infraestrutura, saúde, defesa e instituições competem pelo orçamento;
- abertura comercial e diplomacia afetam relações externas.
Orçamento total dos cinco itens deve ser <= 100. Intensidades devem respeitar os limites do schema.
Explique brevemente a lógica em rationale. Não alegue certeza sobre consequências.
JSON Schema:
{schema}
Retorne somente o objeto JSON.
"""


def parse_decision(raw: str, state: CountryState) -> PolicyDecision:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    decision = PolicyDecision.model_validate_json(text)
    if decision.country_code != state.code or decision.year != state.year + 1:
        raise ValueError("Agent returned a decision for the wrong country or year.")
    return decision
