---
name: traducao-deoc-para-assets
description: Traduz o DEOC (playbook 13) em insumos operacionais por asset — plano de mídia, briefing criativo, LP, copy de anúncios, vendas e tracking — preenchendo a matriz canônica da seção 5.9, briefings derivados, convenção de atributos para UTM/creative ID e backlog de próximos documentos. Use com DEOC aprovado ou consolidado, antes de produzir campanhas, criativos e peças finais.
---

# Tradução DEOC para assets

## Fonte canônica

Playbook **`13_DOSSIE_ESTRATEGICO_OFERTA_COMUNICACAO_CANONICO.md`**, seção **5.9 Tradução para execução**. A tabela oficial define **o que cada saída recebe do DEOC**; esta skill **materializa** essa tradução em texto acionável e, se desejar, em JSON versionável.

## Quando usar

**Depois de:** DEOC com oferta, ICP/anti-ICP, narrativa e claims alinhados (idealmente N2).

**Antes / durante:** plano de mídia, briefings de criativo, redação de LP, variações de anúncio, alinhamento comercial e definição de tracking (UTM, creative ID, eventos).

**Não substitui:** o próprio DEOC nem a skill `dossie-estrategico-oferta-comunicacao` — se algo faltar na fonte, volte ao DEOC em vez de inventar na tradução.

## Inputs (inventário + seção 4 do 13)

- DEOC aprovado ou versão candidata.
- Plano de execução / prioridades de canal (quando já existir rascunho).
- Lista de **assets necessários** no ciclo (o que será produzido neste batch).
- **Taxonomia** ou convenções de UTM / nomenclatura de criativo (projeto pode ter skill dedicada; aqui registramos o mapeamento dos **atributos** exigidos pelo 5.9).

## Princípio (seção 2 do canônico)

Cada asset deve poder ser produzido **sem reinterpretar** promessa, ICP ou prova: copy, design, mídia, LP e vendas leem **esta matriz** (e o DEOC por trás).

## Workflow

1. Confirme versão e link do DEOC em `meta`.
2. Preencha a **matriz resumo** (espelho literal da 5.9) com trechos ou referências às seções do DEOC.
3. Detalhe cada bloco operacional nas subseções (plano de mídia → tracking).
4. Inclua campos de apoio ao criativo (**tom**, **tabus**) quando existir restrição de marca ou compliance — complementam o briefing sem substituir persona/hook/dor/mecanismo/prova/CTA do canônico.
5. Liste **hooks, headlines e CTAs** só com **claims permitidos** ou marcados como teste controlado.
6. Em vendas, amarre **promessa vista pelo lead** ao que mídia/LP realmente prometem.
7. Em tracking, defina dimensões **persona, hook, dor, ângulo, etapa** para UTM/creative ID conforme 5.9.
8. Preencha **próximos documentos** e owner quando a tradução revelar lacunas de produção.
9. Rode `scripts/build_matriz_traducao.py ... --audit` para checar campos obrigatórios do schema.

## Outputs

- Matriz de tradução completa (Markdown ou gerada a partir do JSON).
- Briefings derivados estruturados por asset.
- Tabela de atributos para UTM / creative ID e notas de evento/North Star quando couber.
- Backlog de documentos a criar.

## Artefatos

- `reference.md` — tabela 5.9, requisitos por asset, N2 e anti-padrões.
- `templates/matriz-traducao-deoc.md`
- `templates/matriz-traducao-deoc.json`
- `scripts/build_matriz_traducao.py`

## Scripts

```bash
python3 scripts/build_matriz_traducao.py templates/matriz-traducao-deoc.json --md ./saida-matriz.md
python3 scripts/build_matriz_traducao.py templates/matriz-traducao-deoc.json --audit
```

## Definition of Done

Os **seis blocos** da 5.9 estão preenchidos com insumos que um executor humano ou IA consegue usar sem reabrir o DEOC inteiro; claims e promessas estão **alinhados** ao DEOC; tracking tem dimensões nomeadas para campanha e criativo. Detalhes em `reference.md`.
