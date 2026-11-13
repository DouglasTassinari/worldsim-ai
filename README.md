# WorldSim AI

Simulador geopolítico multiagente: países governados por agentes de IA independentes, com um motor determinístico que aplica as consequências das decisões.

## Estado atual

**MVP — fundação inicial.** O projeto já possui:
- Modelo de estado nacional e decisões estruturadas.
- Motor econômico/demográfico determinístico (sem deixar a IA inventar os resultados).
- Agente mock para executar sem pagar por APIs.
- Interface Streamlit para rodar anos e visualizar indicadores.
- Separação entre agentes, regras de simulação e apresentação.

Integrações reais com OpenAI, Anthropic e Google serão adicionadas em etapas, por adaptadores independentes.

## Executar localmente

Requer Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

O MVP funciona em modo simulado, sem chaves de API.

## Princípios de arquitetura

1. **IA propõe; motor calcula.** Agentes sugerem políticas em formato estruturado. O motor valida e aplica efeitos limitados.
2. **Estado é explícito.** Indicadores e decisões ficam registrados por rodada.
3. **Reprodutibilidade.** O motor não depende de chamadas de IA para calcular consequências.
4. **Provedores intercambiáveis.** Cada integração implementa a interface `CountryAgent`.
5. **Sem falsa precisão.** Os valores iniciais são parâmetros didáticos, não previsões econômicas reais.

## Estrutura

```
worldsim-ai/
├── app.py
├── worldsim/
│   ├── models.py
│   ├── engine.py
│   └── agents/
│       ├── base.py
│       └── mock.py
├── tests/
│   └── test_engine.py
├── requirements.txt
└── .env.example
```

## Próximas etapas

- [ ] Persistência SQLite e histórico de partidas.
- [ ] Adaptadores OpenAI, Anthropic e Gemini.
- [ ] Validação de decisões, limites e eventos aleatórios com seed.
- [ ] Diplomacia bilateral e comércio.
- [ ] Mapa interativo e exportação de linha do tempo.
- [ ] Geração automatizada de vídeos.

## Aviso

WorldSim AI é uma simulação experimental para entretenimento e exploração de cenários. Não é um modelo econômico validado nem ferramenta de previsão ou aconselhamento político.
