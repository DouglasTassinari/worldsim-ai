# Baseline de referência — Brasil e Argentina (2026)

## Fonte principal

**IMF World Economic Outlook (WEO), October 2026**. A base WEO reúne estimativas históricas e projeções, atualizadas conforme informação disponível à equipe do FMI. Os valores de 2026 são projeções/estimativas do vintage publicado em outubro de 2026, não resultados finais observados.

- Dataset: https://www.imf.org/en/Publications/WEO/weo-database/2026/October
- Perfil Brasil: https://www.imf.org/external/datamapper/profile/BRA/WEO
- Perfil Argentina: https://www.imf.org/external/datamapper/profile/ARG/WEO
- Metodologia e ressalvas do WEO: https://www.imf.org/external/datamapper/datasets/WEO

## Parâmetros macro usados no cenário

| Indicador (2026) | Brasil | Argentina | Unidade |
|---|---:|---:|---|
| Crescimento real do PIB | 2,2 | 2,1 | % anual |
| Inflação média ao consumidor | 4,4 | 32,5 | % anual |
| Desemprego | 6,2 | 7,6 | % da força de trabalho |
| População | 214,14 | 47,95 | milhões |
| Dívida bruta do governo geral | 97,0 | 69,3 | % do PIB |
| Saldo do governo geral | -8,1 | 0,4 | % do PIB |
| Conta corrente | -2,4 | 0,6 | % do PIB |

**Importante:** dívida e resultado fiscal referem-se ao governo geral nas séries WEO. O dado de conta corrente é usado como aproximação externa, embora o campo interno `trade_balance` seja uma simplificação do saldo externo e não uma série de comércio de bens.

## Normalização do PIB

O simulador não compara valores nominais em dólares diretamente ao longo do tempo. Define Brasil = 100 e Argentina ≈ 29, calculado pela razão aproximada entre PIB nominal em dólares de 2026 no WEO (Argentina US$ 768,2 bi / Brasil US$ 2,65 tri). É um índice de tamanho relativo, não PIB real.

## Limitações e próximos passos

- O FMI publica projeções; revisões futuras podem alterar a linha de base.
- Índices de educação, infraestrutura, saúde, produtividade, instituições, desigualdade, estabilidade, aprovação e tesouraria são hipóteses de jogo, não medições oficiais.
- Os coeficientes do motor ainda não foram estimados por regressão nem validados por backtesting.
- O modelo de dívida, inflação, câmbio, mercado de trabalho e comércio é simplificado e não captura todas as identidades contábeis.
- Antes de usar cenários como análise de política pública, será necessário calibrar séries históricas, testar previsões fora da amostra, modelar incerteza e comparar múltiplas fontes.

Fonte consultada em 13/11/2026.
