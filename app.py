"""WorldSim AI: assign ideological governors and compare controlled runs."""
import os
import uuid
import pandas as pd
import streamlit as st

from worldsim.agents.profiles import PROFILES
from worldsim.experiments import run_experiment
from worldsim.models import WorldState
from worldsim.scenarios import south_america_2026
from worldsim.storage import SimulationStore

st.set_page_config(page_title="WorldSim AI", page_icon="🌎", layout="wide")
st.title("🌎 WorldSim AI")
st.caption("Simulador geopolítico: países, governantes com ideologias distintas e cenários comparáveis.")

if "world" not in st.session_state:
    st.session_state.world = south_america_2026()
    st.session_state.runs = []

world: WorldState = st.session_state.world
profile_ids = list(PROFILES)

with st.sidebar:
    st.header("Experimento")
    st.write(f"**Cenário:** América do Sul | **Ano inicial:** {world.year}")
    years = st.slider("Duração (anos)", 1, 30, 5)
    seed = st.number_input("Seed dos eventos aleatórios", min_value=0, max_value=999999, value=world.seed)
    model = st.text_input("Modelo OpenAI", value="gpt-4.1-mini")
    demo = st.toggle("Modo demonstração sem API (não usa IA)", value=not bool(os.getenv("OPENAI_API_KEY")))
    if not demo and not os.getenv("OPENAI_API_KEY"):
        st.warning("Defina OPENAI_API_KEY no ambiente para executar agentes ChatGPT.")
    st.divider()
    st.subheader("Governantes por país")
    assignments = {}
    for code, country in world.countries.items():
        selected = st.selectbox(f"{country.name} ({code})", options=profile_ids,
            format_func=lambda key: PROFILES[key].name,
            index=profile_ids.index("social_liberal" if code == "BRA" else "market_liberal"),
            key=f"ideology_{code}")
        assignments[code] = selected
        with st.expander(f"Ver perfil — {PROFILES[selected].name}"):
            st.write(PROFILES[selected].description)
            st.write(f"**Prioridades:** {PROFILES[selected].priorities}")
            st.write(f"**Trade-offs:** {PROFILES[selected].tradeoffs}")
            st.write(f"**Política externa:** {PROFILES[selected].foreign_policy}")
    run = st.button("Executar experimento", type="primary", use_container_width=True, disabled=(not demo and not os.getenv("OPENAI_API_KEY")))
    reset = st.button("Restaurar cenário inicial", use_container_width=True)

if reset:
    st.session_state.world = south_america_2026(seed=int(seed))
    st.session_state.runs = []
    st.rerun()

if run:
    initial = south_america_2026(seed=int(seed))
    try:
        with st.spinner("Governantes tomando decisões e motor calculando consequências..."):
            final_world, history = run_experiment(initial, assignments, int(years), demo=demo, model=model.strip() or "gpt-4.1-mini")
        label = " / ".join(f"{code}: {PROFILES[p].name}" for code, p in assignments.items())
        st.session_state.runs.append({"label": label, "assignments": dict(assignments), "world": final_world, "history": history, "years": int(years), "seed": int(seed)})
        st.session_state.world = final_world
        SimulationStore().save(str(uuid.uuid4()), final_world, history)
        st.success(f"Experimento concluído: {final_world.year}.")
    except Exception as exc:
        st.error(f"Falha na simulação: {exc}")

world = st.session_state.world
st.subheader(f"Estado atual do mundo — {world.year}")
cols = st.columns(len(world.countries))
for col, (code, state) in zip(cols, world.countries.items()):
    with col:
        st.markdown(f"**{state.name} ({code})**")
        st.metric("PIB (índice)", f"{state.gdp_index:.2f}")
        st.metric("Inflação", f"{state.inflation:.1f}%")
        st.metric("Desemprego", f"{state.unemployment:.1f}%")
        st.metric("Aprovação", f"{state.approval:.1f}%")
        st.metric("Dívida / PIB", f"{state.debt_gdp:.1f}%")

if world.relations:
    st.subheader("Relações internacionais")
    for relation in world.relations:
        st.write(f"**{relation.country_a} ↔ {relation.country_b}** | relação {relation.score:.1f}/100 | tarifa {relation.tariff_pct:.1f}% | comércio {relation.trade_volume:.2f}")

if st.session_state.runs:
    st.divider()
    st.subheader("Experimentos desta sessão")
    for index, item in enumerate(st.session_state.runs, start=1):
        with st.expander(f"Experimento {index} — {item['label']}"):
            st.write(f"Duração: {item['years']} anos | Seed: {item['seed']}")
            rows = []
            for rec in item["history"]:
                rows.append({"Ano": rec.year, "País": rec.state.name, "PIB": rec.state.gdp_index, "Inflação": rec.state.inflation, "Desemprego": rec.state.unemployment, "Aprovação": rec.state.approval, "Dívida/PIB": rec.state.debt_gdp, "Crescimento": rec.gdp_growth_pct})
            df = pd.DataFrame(rows)
            metric = st.selectbox("Indicador", ["PIB", "Inflação", "Desemprego", "Aprovação", "Dívida/PIB", "Crescimento"], key=f"metric_{index}")
            st.line_chart(df.pivot(index="Ano", columns="País", values=metric))
            st.write("**Resultado final**")
            for code, state in item["world"].countries.items():
                st.write(f"{state.name}: PIB {state.gdp_index:.2f} | inflação {state.inflation:.1f}% | aprovação {state.approval:.1f}%")
            with st.expander("Decisões dos governantes"):
                for rec in item["history"]:
                    st.markdown(f"**{rec.state.name} — {rec.year}**")
                    st.write(rec.decision.rationale)
                    st.json(rec.decision.model_dump())
                    for event in rec.events:
                        st.warning(event)

st.caption("Modelo experimental. O mesmo modelo OpenAI é usado por todos os governantes; somente os perfis ideológicos e o contexto nacional mudam. O motor, não a IA, calcula os indicadores.")
