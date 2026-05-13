---
name: benchmark-campo-batalha-gtm
description: Mapeia campo de batalha GTM com concorrentes, evidências de mídia e jornada, padrões dominantes, ruído de mercado, gaps, riscos e implicações para assets v1 antes de DEOC, plano de mídia e criativos. Use após handoff e diagnóstico GTM, quando precisar de baseline copiável e diferenciação com lastro.
---

# Benchmark Campo Batalha GTM

## Quando Usar

Use na etapa de inteligência de mercado **antes** de consolidar DEOC, plano de mídia, briefing criativo ou LP.

O benchmark não substitui TAM/SAM/SOM, mapa 2x2, SWOT ou beachhead quando N2 exige esses blocos; ele prepara o terreno e alimenta essas decisões.

Não use como pesquisa infinita ou coleção de exemplos bonitos. Se o achado não muda DEOC, oferta, plano de mídia, criativo, LP ou backlog, ele deve ficar fora do output principal.

## Princípio

Benchmark sem evidência ou sem ligação com decisão vira teatro: **cada achado relevante precisa de lastro** (link, print, data quando couber, nota de fonte).

Antes de executar, a operação deve saber responder:

- qual mercado se tenta capturar;
- quem disputa a mesma atenção;
- quais mensagens estão saturadas;
- onde há brecha de diferenciação;
- qual amostra de concorrentes é válida.

## Inputs Mínimos

- handoff EXECUTAR e contexto do cliente;
- segmento, produto foco, ticket, geografia;
- ICP ou persona preliminar;
- lista inicial de concorrentes (tipicamente 3 a 10) e/ou keywords de descoberta;
- canais de interesse e objetivo de aquisição.

## Fluxo De Trabalho

1. Definir escopo e pergunta de negócio que o benchmark precisa destravar.
2. Selecionar amostra: diretos, substitutos e referências fortes do setor (evitar irrelevante).
3. Coletar evidências por player (ordem recomendada): biblioteca de anúncios → busca/SERP e LPs → redes → reviews → oferta e prova.
4. Consolidar padrões que se repetem no setor.
5. Montar matriz força vs. fraco e **gaps exploráveis** por concorrente.
6. Listar **ruído de mercado** (promessas saturadas).
7. Converter em decisões: baseline a adotar vs. onde diferenciar vs. riscos a mitigar.
8. Registrar implicações para pacote de assets v1, oferta/comunicação, mídia e criativos.
9. Separar opinião de evidência: links/prints/datas sustentam o que entra como padrão; hipóteses sem lastro viram pergunta ou backlog, não conclusão.

## Output Esperado

- mapa do campo de batalha com evidências;
- tabela de concorrentes auditados;
- padrões acionáveis (cerca de 5 a 15 bullets);
- ruídos listados;
- gaps e riscos;
- implicações para v1.

Use `templates/benchmark-gtm.md`.
Use `templates/benchmark-gtm.json` com o script para gerar Markdown resumido a partir de dados estruturados.

## Script Utilitário

```bash
python3 scripts/build_benchmark_gtm.py templates/benchmark-gtm.json --md /tmp/benchmark-gtm.md
```

## Definition Of Done

- Amostra e critérios de escolha estão documentados.
- Evidências são rastreáveis.
- Há síntese de padrões, oportunidades e riscos.
- Saída aponta implicações para próximos assets e testes.
