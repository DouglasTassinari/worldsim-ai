# WorldSim AI

Simulador geopolítico multiagente. Governos são representados por agentes independentes (LLMs ou agentes demonstrativos); um motor separado calcula os efeitos das políticas, mantém o estado do mundo e registra a evolução anual.

> **Limite científico:** este projeto é um laboratório experimental, não um modelo macroeconômico calibrado nem ferramenta de previsão. Os parâmetros iniciais são hipóteses normalizadas para gameplay. Realismo exige calibração com séries históricas, validação retrospectiva e análise de sensibilidade.

## O que existe nesta branch

- Estado nacional com PIB indexado, população, inflação, desemprego, dívida/PIB, resultado fiscal, comércio, câmbio, capital humano, infraestrutura, saúde, produtividade, desigualdade, instituições, estabilidade e aprovação.
- Decisões governamentais estruturadas, com orçamento limitado e políticas tributária, monetária, social, investimento, defesa, comércio e diplomacia.
- Motor determinístico com choques pseudoaleatórios reproduzíveis por seed.
- Relações bilaterais com índice de confiança, tarifas e volume comercial.\n- Choques globais reproduzíveis (desaceleração, energia, estresse financeiro, crise sanitária, tecnologia e clima), com probabilidades explicitamente tratadas como hipóteses de jogo.
- Cenário inicial demonstrativo Brasil–Argentina (valores ilustrativos, não retrato estatístico oficial).
- Agentes plugáveis: demo local, OpenAI, Anthropic e Gemini.
- Persistência SQLite de snapshots anuais.
- Dashboard Streamlit com comparação de indicadores, gráfico temporal e diário de eventos.
- Testes automatizados para regras, limites, diplomacia e reprodutibilidade.

## Executar

Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

O modo **Demo (gratuito)** não chama serviços externos.

## Conectar modelos de IA

Instale os SDKs opcionais:

```bash
pip install -r requirements-llm.txt
```

Configure as variáveis de ambiente (nunca coloque chaves no Git):

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`

Selecione o provedor de cada país na barra lateral. Chamadas reais podem gerar custos conforme modelo e quantidade de anos. Comece com 1 ano e monitore o consumo.

Modelos padrão configuráveis no código:
- OpenAI: `gpt-4.1-mini`
- Anthropic: `claude-sonnet-4-5`
- Google: `gemini-2.5-flash`

## Arquitetura

```
app.py                         # interface Streamlit
worldsim/
  models.py                    # contratos Pydantic e estado do mundo
  engine.py                    # regras determinísticas e atualização anual
  scenarios.py                 # cenários de partida
  storage.py                   # snapshots SQLite
  agents/
    base.py                    # contrato comum
    mock.py                    # agente sem custo
    prompting.py               # prompt e validação de saída
    openai_agent.py             # adaptador OpenAI
    anthropic_agent.py          # adaptador Anthropic
    google_agent.py             # adaptador Gemini
tests/                         # testes automatizados
.github/workflows/tests.yml    # CI
```

## Princípios de modelagem

1. **Agente decide; motor aplica.** O LLM não pode alterar PIB, inflação ou população diretamente.
2. **Orçamento limitado.** As alocações não podem ultrapassar 100 pontos.
3. **Separação de decisão e consequência.** Políticas são entradas; os resultados são calculados pelo motor.
4. **Reprodutibilidade.** Choques pseudoaleatórios são determinísticos para seed, país e ano.
5. **Relações bilaterais.** Diplomacia altera relação, tarifas e comércio de forma simplificada.
6. **Transparência.** Coeficientes são explícitos e devem ser calibrados antes de qualquer alegação de realismo empírico.

## Próximas prioridades de pesquisa e engenharia

- Completar a calibração das variáveis estruturais com dados oficiais (Banco Mundial, FMI, bancos centrais e institutos nacionais), com fonte, data e unidade por variável.
- Estimar coeficientes usando séries históricas e backtesting; documentar incerteza.
- Implementar bancos centrais independentes, eleições, coalizões, parlamentos, choques externos, commodities, dívida em moeda estrangeira e risco soberano.
- Modelar comércio bilateral por setor, cadeias de suprimento, sanções, migração e alianças.
- Introduzir população por faixa etária, produtividade setorial e distribuição de renda.
- Adicionar logs de prompts/respostas com proteção de segredos, retries, limites de custo e avaliação de qualidade dos agentes.
- Criar mapa territorial e exportação de narrativas/vídeos.

## Aviso

WorldSim AI é uma simulação experimental de entretenimento e pesquisa exploratória. Não representa previsões, recomendações de política pública ou avaliação oficial de países.
