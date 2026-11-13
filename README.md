# WorldSim AI

Simulador geopolítico multiagente. Cada país é governado por um agente baseado em OpenAI, com perfil ideológico independente. O usuário pode trocar governantes entre países, executar cenários e comparar resultados.

> **Limite científico:** laboratório experimental, não modelo macroeconômico calibrado nem ferramenta de previsão. Coeficientes e indicadores estruturais ainda exigem calibração histórica.

## Conceito central

- **País:** território, população, economia, recursos, instituições e situação inicial.
- **Governante:** perfil ideológico reutilizável, independente do país.
- **Simulação:** regras, eventos, seed e estado inicial.
- **Experimento:** cópia do mesmo cenário inicial com uma distribuição específica de governantes.

Todos os governantes reais usam o mesmo modelo OpenAI. A ideologia altera prioridades, trade-offs e política externa; o contexto e as restrições do país continuam sendo considerados. Anthropic e Gemini não fazem parte desta fase.

## Perfis disponíveis

- Social-democrata
- Liberal de mercado
- Nacionalista
- Socialista
- Autoritário desenvolvimentista
- Ecologista

Os perfis são pontos de partida simplificados, não retratos completos de movimentos políticos reais.

## Executar localmente

Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
pip install -r requirements-llm.txt
export OPENAI_API_KEY="sua-chave"  # PowerShell: $env:OPENAI_API_KEY="sua-chave"
streamlit run app.py
```

O modo demonstração permite testar a interface e o motor sem chamadas de IA. Para governantes ChatGPT reais, configure OPENAI_API_KEY. O uso da API é cobrado separadamente da assinatura ChatGPT.

## Comparação justa

Para comparar ideologias, mantenha iguais cenário e indicadores iniciais, duração e seed dos eventos globais. Altere somente a distribuição de governantes. Assim, diferenças observadas ficam menos contaminadas por condições iniciais distintas. Chamadas de IA podem variar entre execuções; para comparações científicas, registre modelo, parâmetros e decisões geradas.

## Arquitetura

```
app.py
worldsim/
  models.py
  engine.py
  events.py
  scenarios.py
  experiments.py
  storage.py
  agents/
    base.py
    factory.py
    profiles.py
    prompting.py
    openai_agent.py
tests/
```

## Princípios

1. **Agente decide; motor calcula.** O LLM propõe políticas estruturadas, não altera diretamente os indicadores.
2. **País não é ideologia.** O mesmo perfil pode governar qualquer país.
3. **Experimentos partem de cópias independentes.**
4. **Reprodutibilidade explícita.** Eventos usam seed; decisões de IA não são determinísticas.
5. **Transparência.** Parâmetros são hipóteses de jogo até serem calibrados e validados.

## Aviso

WorldSim AI é uma simulação experimental para exploração de cenários e entretenimento. Não representa previsões, recomendações de política pública ou avaliação oficial de países.
