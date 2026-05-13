---
name: gerador-taxonomia-utm-ids
description: Gera IDs canônicos, nomes de campanha/ad group/criativo, UTMs completas e parâmetros v4 para campanhas de leadgen. Use antes de setup Meta Ads, Google Ads, LP, plano de mídia, briefing criativo, tracking, CRM ou quando o usuário pedir nomenclatura, UTMs, campaign_id, creative_id, adgroup_id ou URLs parametrizadas.
---

# Gerador Taxonomia UTM IDs

## Quando Usar

Use quando precisar criar:

- `client_id`, `campaign_id`, `adgroup_id`, `creative_id` e `test_id`;
- nomes visíveis para campanha, conjunto/ad group e criativo;
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`;
- parâmetros `v4_*`;
- URLs finais parametrizadas;
- tabela de UTMs para mídia, LP, CRM e planilha de testes.

Nao use para auditar tracking depois do go-live. Para isso, use a futura skill `qa-tracking-utm-crm`.

## Inputs Necessários

- Cliente e slug do cliente.
- Ano/mês e sequenciais desejados.
- Canal e tipo de mídia.
- Tipo de campanha, objetivo, movimento, cohort, segmento e período.
- Público/ad group: público, temperatura, posicionamento, keyword/match quando Search, placement e geo.
- Criativo: formato, hook, persona, slug, dor, ângulo, etapa e versão.
- Teste: hipótese ou `test_id`.
- URL base da LP ou ponto de conversão.

Se algum valor estiver solto ou com acento/espaço, normalize para slug antes de gerar.

## Workflow

1. Confirme o escopo: uma campanha, vários criativos, Search, social, LP, WhatsApp ou outro ponto.
2. Normalize todos os valores:
   - minúsculas;
   - sem acentos;
   - sem espaços;
   - `-` entre palavras;
   - valores curtos e estáveis.
3. Gere IDs:
   - `cli-{slug_cliente}`;
   - `cmp-{cliente}-{ano}{mes}-{sequencial}`;
   - `adg-{cliente}-{ano}{mes}-{sequencial}`;
   - `crv-{cliente}-{ano}{mes}-{sequencial}`;
   - `tst-{cliente}-{ano}{mes}-{sequencial}`.
4. Monte nomes visíveis:
   - campanha: `{campaign_id} | {tipo_campanha} | {objetivo} | {movimento} | {slug}`;
   - ad group: `{adgroup_id} | {publico} | {temperatura} | {posicionamento} | {slug}`;
   - criativo: `{creative_id} | {formato} | {hook} | {persona} | {slug} | {versao}`.
5. Monte UTMs:
   - `utm_campaign` com campanha, tipo, objetivo, movimento, slug, cohort, segmento e período;
   - `utm_content` com criativo, formato, hook, persona, slug, dor, ângulo, etapa e versão;
   - `utm_term` social ou search conforme o caso.
6. Adicione parâmetros `v4_client_id`, `v4_campaign_id`, `v4_adgroup_id`, `v4_creative_id`, `v4_test_id`.
7. Gere URL final e tabela para planilha.
8. Valide se IDs e nomes são curtos, parseáveis e coerentes com plano de mídia/briefing.

## Output Esperado

Produza:

- IDs canônicos;
- nomes visíveis;
- UTMs completas;
- parâmetros customizados;
- URL final;
- tabela por campanha/ad group/criativo;
- observações de risco se algum campo estiver genérico, longo ou ausente.

Use `templates/url-utm.md` para documentação manual.
Use `templates/campanha-utm.json` com o script para gerar outputs em lote.

## Script Utilitário

Para gerar CSV e Markdown a partir de JSON:

```bash
python scripts/generate_utm_matrix.py templates/campanha-utm.json --csv /tmp/utm.csv --md /tmp/utm.md
```

O script normaliza valores, monta IDs, nomes, UTMs e URLs. Revise o output antes de publicar campanhas.

## Definition Of Done

- Toda campanha tem `campaign_id`.
- Todo ad group/conjunto tem `adgroup_id`.
- Todo criativo tem `creative_id`.
- Toda URL tem UTMs completas e parâmetros `v4_*`.
- Nomes visíveis têm ID + 3 a 5 dimensões humanas.
- Campos são parseáveis por `__` e `chave-valor`.
- Valores genéricos ou longos foram corrigidos.

## Armadilhas

- Criar nomes enormes para análise que deveria estar nos subparâmetros.
- Usar acentos, espaços, maiúsculas ou frases.
- Misturar campanha, ad group e criativo no mesmo campo.
- Publicar criativo sem `creative_id`.
- Criar UTM sem `v4_*` quando CRM/planilha pode receber campos próprios.
- Usar valores livres demais que impedem agrupamento.

## Referências

- Playbook canônico: `assets/canonicos/01_TAXONOMIA_UTM_IDS_E_SUBPARAMETROS.md`
- Detalhamento: `reference.md`
- Template: `templates/url-utm.md`
- Schema: `templates/campanha-utm.json`
