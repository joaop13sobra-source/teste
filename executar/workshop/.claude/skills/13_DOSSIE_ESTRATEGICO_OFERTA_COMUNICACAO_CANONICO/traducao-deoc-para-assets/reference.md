# Referência — Tradução DEOC para assets

Norma principal: **`13_DOSSIE_ESTRATEGICO_OFERTA_COMUNICACAO_CANONICO.md`**, seção **5.9**.

## Matriz canônica (texto oficial)

O DEOC deve terminar com uma matriz:

| Saída | O que recebe do DEOC |
| --- | --- |
| Plano de mídia | beachhead, canais prováveis, ângulos, premissas, ICP/anti-ICP, oferta e critérios de lead correto |
| Briefing criativo | persona, hook, dor, mecanismo, prova e CTA |
| LP | narrativa, seções, promessa, prova, objeções, formulário, escopo e CTA |
| Copy de anúncios | hooks, headlines, CTAs, variações e claims |
| Vendas | promessa vista pelo lead, objeções, anti-ICP, perguntas de qualificação e limites da oferta |
| Tracking | atributos para UTM/creative ID: persona, hook, dor, ângulo, etapa |

Esta skill **expande** cada linha em campos preenchíveis e liga ao **backlog** de peças ainda não existentes.

## Mapeamento sugerido (DEOC → asset)

| Fonte no DEOC (playbook 13) | Uso típico |
| --- | --- |
| 5.1 Resumo / beachhead | Plano de mídia, priorização de mensagem |
| 5.2 Oferta e mecanismo | Plano de mídia, LP, copy, vendas (expectativa) |
| 5.3 ICP / anti-ICP | Segmentação, exclusões, qualificação, vendas |
| 5.4 Problemas | Hook, dor, ângulos |
| 5.5 Alternativas | Objeções LP, vendas |
| 5.6 Proposta de valor | Headlines, hero LP |
| 5.7 Narrativa | Storyline LP, criativo |
| 5.8 Claims | Tudo que é texto público; só permitidos ou teste explícito |
| 5.9 (esta tradução) | Handoff para produção |

## Campos obrigatórios do schema JSON (auditoria)

Para passar em `--audit`, cada bloco deve ter texto ou listas não vazias nos campos que o canônico lista:

- **Plano de mídia:** beachhead, canais prováveis, ângulos, premissas, ICP/anti-ICP, oferta, critérios de lead correto.
- **Briefing criativo:** persona, hook, dor, mecanismo, prova, CTA (tom e tabus recomendados se houver compliance).
- **LP:** narrativa, seções, promessa, prova, objeções, formulário, escopo, CTA.
- **Copy de anúncios:** pelo menos um item em hooks, headlines e CTAs; variações e claims explícitos.
- **Vendas:** promessa vista pelo lead, objeções, anti-ICP, perguntas de qualificação, limites da oferta.
- **Tracking:** persona, hook, dor, ângulo, etapa (dimensões para UTM/creative ID).

## N2 (trecho relevante do playbook 13, seção 6)

O DEOC (e portanto sua tradução) dialoga com N2 quando **orienta mídia, criativo, LP e vendas**. Tradução incompleta ou genérica (“ver DEOC”) viola o espírito do critério **“pode ser usado por IA e humanos sem recoletar contexto”**.

## O que evitar (seção 8 + 5.9)

- Matriz só com títulos, sem conteúdo acionável.
- Headline ou hook com **claim proibido** ou sem âncora quando o DEOC exige prova.
- LP ou anúncio **desconectados** da promessa que vendas assumem.
- Tracking sem dimensões alinhadas a persona, mensagem e etapa — impossibilita aprendizado por ângulo.

## Legado

Playbooks **04 (DCC)** e **10 (UCM)** podem inspirar formato de briefing antigo; a **fonte de verdade** continua sendo o DEOC e a matriz **5.9**.
