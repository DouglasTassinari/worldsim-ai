"""Streamlit MVP for WorldSim AI."""
import streamlit as st
from worldsim.agents.mock import MockAgent
from worldsim.engine import SimulationEngine
from worldsim.models import CountryState

st.set_page_config(page_title="WorldSim AI", page_icon="🌎", layout="wide")
st.title("WorldSim AI")
st.caption("Simulação geopolítica multiagente — protótipo experimental")

if "states" not in st.session_state:
    st.session_state.states = {
        "BRA": CountryState(name="Brasil", code="BRA", gdp_index=100, inflation=4.5,
                            unemployment=7.5, approval=52, education=55,
                            infrastructure=48, defense=52, treasury=55),
        "ARG": CountryState(name="Argentina", code="ARG", gdp_index=75, inflation=8,
                            unemployment=9, approval=48, education=53,
                            infrastructure=45, defense=45, treasury=38),
    }
    st.session_state.history = []

st.info("Nesta primeira versão, os países usam agentes demonstrativos locais. Nenhuma API é chamada.")
cols = st.columns(len(st.session_state.states))
for col, (code, state) in zip(cols, st.session_state.states.items()):
    with col:
        st.subheader(state.name)
        st.metric("Ano", state.year)
        st.metric("PIB (índice)", f"{state.gdp_index:.2f}")
        st.metric("Inflação", f"{state.inflation:.1f}%")
        st.metric("Desemprego", f"{state.unemployment:.1f}%")
        st.metric("Aprovação", f"{state.approval:.1f}%")
        st.metric("Educação", f"{state.education:.1f}")
        st.metric("Infraestrutura", f"{state.infrastructure:.1f}")

st.divider()
years = st.slider("Anos por rodada", min_value=1, max_value=10, value=1)
if st.button("Simular próximos anos", type="primary"):
    engine = SimulationEngine()
    for _ in range(years):
        for code, state in list(st.session_state.states.items()):
            style = "growth" if code == "BRA" else "balanced"
            decision = MockAgent(style).decide(state)
            record = engine.advance(state, decision)
            st.session_state.states[code] = record.state
            st.session_state.history.append(record)
    st.rerun()

if st.session_state.history:
    st.subheader("Histórico de decisões")
    for record in reversed(st.session_state.history[-10:]):
        with st.expander(f"{record.state.name} — {record.year}"):
            st.write(record.decision.rationale)
            st.json(record.decision.model_dump())
