"""Interactive multi-country simulation dashboard."""
import os
import uuid
import streamlit as st
import pandas as pd

from worldsim.agents.mock import MockAgent
from worldsim.engine import SimulationEngine
from worldsim.models import WorldState
from worldsim.scenarios import south_america_2026
from worldsim.storage import SimulationStore

st.set_page_config(page_title="WorldSim AI", page_icon="🌎", layout="wide")
st.title("🌎 WorldSim AI")
st.caption("Laboratório de simulação geopolítica multiagente | protótipo experimental")

if "world" not in st.session_state:
    st.session_state.world = south_america_2026()
    st.session_state.records = []
    st.session_state.run_id = str(uuid.uuid4())

world: WorldState = st.session_state.world

def make_agent(provider: str, code: str):
    if provider == "OpenAI":
        from worldsim.agents.openai_agent import OpenAIAgent
        return OpenAIAgent()
    if provider == "Anthropic":
        from worldsim.agents.anthropic_agent import AnthropicAgent
        return AnthropicAgent()
    if provider == "Google Gemini":
        from worldsim.agents.google_agent import GoogleAgent
        return GoogleAgent()
    styles = {"BRA": "growth", "ARG": "balanced"}
    return MockAgent(styles.get(code, "balanced"))

with st.sidebar:
    st.header("Configuração")
    st.write(f"**Ano da simulação:** {world.year}")
    years = st.slider("Anos a simular", 1, 20, 1)
    st.caption("Agentes reais fazem chamadas pagas às APIs. O modo demonstrativo não gera custo.")
    providers = {}
    for code, country in world.countries.items():
        providers[code] = st.selectbox(
            f"Agente — {country.name}",
            ["Demo (gratuito)", "OpenAI", "Anthropic", "Google Gemini"],
            key=f"provider_{code}",
        )
    run = st.button("Executar simulação", type="primary", use_container_width=True)
    reset = st.button("Reiniciar cenário", use_container_width=True)

if reset:
    st.session_state.world = south_america_2026()
    st.session_state.records = []
    st.session_state.run_id = str(uuid.uuid4())
    st.rerun()

if run:
    engine = SimulationEngine(seed=world.seed)
    store = SimulationStore()
    progress = st.progress(0)
    status = st.empty()
    for step in range(years):
        decisions = {}
        try:
            for code, state in st.session_state.world.countries.items():
                provider = providers[code]
                if provider != "Demo (gratuito)":
                    key_name = {"OpenAI": "OPENAI_API_KEY", "Anthropic": "ANTHROPIC_API_KEY",
                                "Google Gemini": "GOOGLE_API_KEY"}[provider]
                    if not os.getenv(key_name):
                        raise RuntimeError(f"Configure {key_name} no ambiente antes de selecionar {provider}.")
                agent = make_agent(provider, code)
                context = "Relações bilaterais: " + "; ".join(
                    f"{r.country_a}-{r.country_b}: relação {r.score:.0f}/100, tarifa {r.tariff_pct:.1f}%"
                    for r in st.session_state.world.relations
                )
                decisions[code] = agent.decide(state, context)
            next_world, records = engine.advance_world(st.session_state.world, decisions)
            st.session_state.world = next_world
            st.session_state.records.extend(records)
            store.save(st.session_state.run_id, next_world, records)
            progress.progress((step + 1) / years)
            status.success(f"Ano {next_world.year} concluído.")
        except Exception as exc:
            status.error(f"Simulação interrompida: {exc}")
            break
    st.rerun()

world = st.session_state.world
cols = st.columns(len(world.countries))
for col, (code, state) in zip(cols, world.countries.items()):
    with col:
        st.subheader(f"{state.name} ({code})")
        st.metric("PIB — índice", f"{state.gdp_index:.2f}")
        st.metric("Inflação", f"{state.inflation:.1f}%")
        st.metric("Desemprego", f"{state.unemployment:.1f}%")
        st.metric("Aprovação", f"{state.approval:.1f}%")
        st.metric("Dívida / PIB", f"{state.debt_gdp:.1f}%")
        st.metric("Crescimento populacional", f"{state.population_m:.1f} mi hab.")
        with st.expander("Indicadores estruturais"):
            for label, value in [
                ("Educação", state.education), ("Saúde", state.health),
                ("Infraestrutura", state.infrastructure), ("Produtividade", state.productivity),
                ("Instituições", state.institutions), ("Desigualdade (índice)", state.inequality),
                ("Estabilidade", state.stability), ("Resultado fiscal / PIB", state.fiscal_balance),
                ("Balança comercial / índice", state.trade_balance),
            ]:
                st.write(f"**{label}:** {value:.2f}")

st.divider()
st.subheader("Relações internacionais")
if world.relations:
    for relation in world.relations:
        st.write(f"**{relation.country_a} ↔ {relation.country_b}**")
        a, b, c = st.columns(3)
        a.metric("Relação bilateral", f"{relation.score:.1f}/100")
        b.metric("Tarifa simulada", f"{relation.tariff_pct:.1f}%")
        c.metric("Volume comercial (índice)", f"{relation.trade_volume:.2f}")

if st.session_state.records:
    st.divider()
    st.subheader("Evolução histórica")
    rows = []
    for rec in st.session_state.records:
        rows.append({"Ano": rec.year, "País": rec.state.name, "PIB": rec.state.gdp_index,
                     "Inflação": rec.state.inflation, "Desemprego": rec.state.unemployment,
                     "Aprovação": rec.state.approval, "Dívida/PIB": rec.state.debt_gdp,
                     "Crescimento": rec.gdp_growth_pct})
    df = pd.DataFrame(rows)
    metric = st.selectbox("Indicador para comparar", ["PIB", "Inflação", "Desemprego",
        "Aprovação", "Dívida/PIB", "Crescimento"])
    chart = df.pivot(index="Ano", columns="País", values=metric)
    st.line_chart(chart)
    with st.expander("Diário de decisões e eventos", expanded=True):
        for rec in reversed(st.session_state.records):
            with st.expander(f"{rec.state.name} — {rec.year} | crescimento {rec.gdp_growth_pct:.2f}%"):
                st.write(rec.decision.rationale)
                st.json(rec.decision.model_dump())
                for event in rec.events:
                    st.warning(event)

st.caption("Modelo estilizado para exploração de cenários. Coeficientes e valores iniciais são hipóteses de jogo, não estimativas oficiais nem previsões.")
