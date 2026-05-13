---
name: funil-unificado-conversoes-a2
description: Desenha o Funil Unificado (A-2) com etapas, definições únicas Marketing+Vendas, eventos, fonte da verdade por etapa, campos mínimos, handoffs e backlog — antes do contrato de dados, CRM/SLA e setup de campanhas. Fonte playbook 17. Saída consolidada em Markdown via JSON e auditoria de DoD.
---

# Funil unificado — conversões (A-2)

## Fonte canônica

Playbook **`17_FUNIL_UNIFICADO_CONVERSOES_A2_CANONICO.md`** (e legado `04-funil-unificado-a2.md` alinhado ao mesmo conteúdo).

## Propósito (1 frase)

Definir o fluxo end-to-end do lead (geração → venda/drop) com **vocabulário único** e **fonte da verdade** por etapa, para tracking, CRM e otimização não competirem entre áreas.

## Quando usar / quando não

**Usar** antes de fechar Plano de Mídia, antes de implementar tracking/CRM como fonte da verdade, ou quando há definições conflitantes entre áreas. **Não usar** para redesenhar organograma — foco é fluxo, definições e evidência (§ “Quando usar”).

## Entradas

Plano de mídia; DEOC; AS IS (comercial, time, ferramentas); benchmark de conversão por etapa; objetivo de conversão e “lead correto” (§ Entradas).

## Dependências recomendadas

- **`benchmark-campo-batalha-gtm`** ou materiais de benchmark do segmento (faixas por etapa).
- **`contrato-dados-marketing-crm`** — aplicado **depois** que o funil v1 existir.
- **`protocolo-handoff-mql-sql-a4`** — vincular `link_protocolo_handoff` / artefato A-4 quando existir (playbook 18).
- **`jornada-lead-raci`** — donos R/A/C/I e touchpoints por etapa (playbook 19); complementa governança pós-definição do funil.

## Workflow (passos 1–7 do canônico)

1. Objetivo do funil: conversão final que importa + definição de lead correto.
2. AS IS Marketing e Vendas: origem, atendimento, perdas e sumiço de lead.
3. TO BE: etapas propostas e **um nome/ Definição por etapa** alinhados entre áreas.
4. Por etapa: critério “passou”, evidência mínima, faixa verde/amarelo/vermelho (com fonte), **uma** fonte da verdade, campos mínimos com regra de preenchimento; handoffs.
5. Eventos de tracking necessários para sustentar o funil.
6. Coerência com capacidade do time e ciclo (funil operável).
7. Publicar artefato + **backlog** (campos, integrações, treino, adoção).

Em paralelo, preencher **`templates/funil-unificado-a2.json`** (recomendado) e gerar o Markdown de leitura:

```bash
python3 scripts/build_funil_unificado_a2.py templates/funil-unificado-a2.json --md ./funil-unificado-a2-consolidado.md
python3 scripts/build_funil_unificado_a2.py templates/funil-unificado-a2.json --audit
```

Quem preferir editar em prosa pode usar **`templates/funil-unificado-a2.md`** como espelho das seções e depois transcrever para o JSON.

## Outputs (funil v1)

Etapas com definição; evento que “conta”; taxas aceitáveis (faixas); fonte da verdade; campos mínimos; pontos de handoff ligados ao protocolo — conforme § Saídas do playbook.

## Definition of Done (playbook)

Etapas nomeadas e definidas com acordo Mkt+Vendas; fonte da verdade **uma por etapa**; campos mínimos com definição; handoffs identificados; backlog priorizado (§ DoD).

## Gerenciamento contínuo

KPIs sugeridos, thresholds e cadência quinzenal→mensal estão no JSON (`gerenciado`) e no `reference.md`. **Change log** obrigatório para mudanças: skill **`changelog-funil-conversoes`**. **Rodadas de governança:** após publicar o A-2, usar **`auditoria-funil-fontes-verdade`** na cadência do § Gerenciado (playbook 17).

## Artefatos

- `reference.md` — mapa § playbook ↔ campos do template.
- `templates/funil-unificado-a2.md`
- `templates/funil-unificado-a2.json`
- `scripts/build_funil_unificado_a2.py`
