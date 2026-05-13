# Referência — Funil unificado A-2 ↔ playbook 17

Canônico: `17_FUNIL_UNIFICADO_CONVERSOES_A2_CANONICO.md`.

## Passo a passo (playbook) ↔ JSON

| Passo | Seção implícita | Campos principais no JSON |
|-------|------------------|---------------------------|
| 1 Objetivo do funil | Passo 1 | `objetivo.conversao_final_que_importa`, `objetivo.lead_correto_definicao` |
| 2 AS IS | Passo 2 | `as_is.marketing`, `as_is.vendas`, `as_is.ferramentas_resumo`, `as_is.lacunas` |
| 3 TO BE / vocabulário | Passo 3 | `to_be.notas_alinhamento`, nomes em `etapas[].nome` |
| 4 Por etapa | Passo 4 | `etapas[]`: `definicao_passa`, `evidencia_minima`, `taxa_aceitavel`, `fonte_da_verdade`, `campos_minimos`, `handoff_protocolo_ref` |
| 5 Eventos tracking | Passo 5 | `eventos_tracking[]` |
| 6 Coerência operação | Passo 6 | `coerencia_operacao` |
| 7 Backlog | Passo 7 | `backlog[]` |

## Saídas do playbook ↔ estrutura

| Saída canônica | Onde no JSON |
|----------------|--------------|
| Etapas nome + definição | `etapas[].nome`, `definicao_passa` |
| Evento de conversão por etapa | `etapas[].conversao_evento` (+ `eventos_tracking` agregado) |
| Taxa aceitável (faixas) | `etapas[].taxa_aceitavel.{verde,amarelo,vermelho,fonte_benchmark}` |
| Fonte da verdade | `etapas[].fonte_da_verdade` |
| Campos mínimos | `etapas[].campos_minimos[]` |
| Handoffs | `etapas[].handoff_protocolo_ref`, `meta.link_protocolo_handoff` |

## Componentes críticos (iteração)

Conforme playbook: definições operacionais vs nome cosmético; **uma** fonte da verdade; poucos campos essenciais; alinhamento Plano de Mídia; funil cabível na operação.

## Gerenciado (playbook § final)

- **KPIs:** % leads com status válido; % campos mínimos preenchidos; tempo de ciclo por etapa.
- **Vermelho:** discrepância entre fontes ou etapa sem dono.
- **Amarelo:** muitas etapas, baixa adesão de dados.
- **Verde:** rastreio mínimo e aderência.
- **Cadência:** quinzenal até estabilizar; mensal depois; mudanças no change log.

Campos `gerenciado` no JSON espelham isso; preencher `dono_funil` quando a lacuna “Dono” do canônico for fechada.

## Auditoria (`--audit`)

O script verifica preenchimento mínimo para o DoD: meta, objetivo, AS IS, ≥2 etapas com bloco completo, eventos de tracking, coerência operacional e backlog não vazio. Itens listados são **lacunas** até preencher ou justificar em notas (fora do escopo do script).
