---
name: tese-estrategica-ucm
description: Organiza tese estratégica UCM com contexto, problema, persona, alternativa percebida, proposta de valor, mecanismo, inimigo, provas, narrativa central e tradução para ativos. Use quando o usuário mencionar UCM, planejamento estratégico de comunicação, tese de campanha ou quando for preciso alimentar DEOC, LP, mídia, criativos e vendas.
---

# Tese Estratégica UCM

## Quando Usar

Use depois de discovery e antes de DEOC, plano de mídia, briefing criativo, LP, script comercial ou taxonomia de testes.

Também use retroativamente quando DCC, LP ou campanhas nasceram de frases soltas e precisam de uma tese estratégica auditável.

## Inputs

- handoff sales-to-ops;
- discovery;
- site e materiais comerciais;
- histórico de campanhas;
- feedback de vendas;
- objeções reais;
- provas, cases e números;
- concorrentes e alternativas percebidas;
- restrições jurídicas, técnicas e comerciais.

## Estrutura Mínima

1. Contexto do negócio.
2. Problemas priorizados.
3. Personas e papéis de decisão.
4. Alternativas percebidas.
5. Frequência natural do problema.
6. Proposta de valor e mecanismo.
7. Inimigo/status quo.
8. Provas e autoridade.
9. Narrativa central.
10. Vocabulário estratégico.
11. Tradução para ativos.

## Workflow

1. Declare a batalha estratégica antes da copy.
2. Priorize problemas com impacto e voz do cliente.
3. Separe personas e papéis de decisão.
4. Mapeie alternativas percebidas e por que falham.
5. Formule proposta de valor:

```text
Para [persona], que sofre com [problema], [produto/oferta] entrega [resultado] por meio de [mecanismo], sem [objeção], comprovado por [prova].
```

6. Defina inimigo/status quo.
7. Separe provas de claims pendentes.
8. Escreva narrativa central.
9. Traduza para DCC/DEOC, LP, criativos, mídia, comercial e tracking.

## Output Esperado

- tese estratégica resumida;
- problemas priorizados;
- narrativa central;
- proposta de valor;
- matriz de tradução para ativos;
- claims pendentes;
- próximos insumos para DEOC.

Use `templates/tese-ucm.md`.
Use `templates/tese-ucm.json` com o script para montar uma versão inicial.

## Script Utilitário

```bash
python3 scripts/build_ucm_thesis.py templates/tese-ucm.json --md /tmp/tese-ucm.md
```

## Definition Of Done

- A tese responde qual batalha está sendo travada.
- Problemas têm impacto e voz do cliente.
- Persona tem papel decisório.
- Proposta de valor tem mecanismo.
- Promessa forte aponta para prova ou claim pendente.
- Saída orienta ativos executáveis.
