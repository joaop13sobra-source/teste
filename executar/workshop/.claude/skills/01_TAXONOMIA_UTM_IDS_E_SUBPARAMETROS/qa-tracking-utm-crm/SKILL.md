---
name: qa-tracking-utm-crm
description: Valida se UTMs, IDs, first-touch, last-touch, planilha backup e CRM preservam a origem do lead de ponta a ponta. Use antes de go-live, depois de lead teste, em QA de LP/formulário/WhatsApp, setup Meta Ads, Google Ads, contrato de dados ou quando houver suspeita de tracking quebrado.
---

# QA Tracking UTM CRM

## Quando Usar

Use para validar a ponte:

```text
URL com UTMs -> LP/ponto de conversão -> formulário/WhatsApp -> planilha backup -> CRM -> análise
```

Use especialmente:

- antes de ativar verba;
- depois de criar campanha em rascunho;
- antes de considerar tracking N2;
- quando leads chegam sem origem;
- quando CRM e planilha não batem;
- quando há dúvida sobre first-touch, last-touch, `creative_id` ou dedupe.

## Inputs Necessários

- URL final com UTMs e parâmetros `v4_*`.
- Registro do lead teste na LP/formulário/WhatsApp.
- Linha da planilha backup.
- Registro do CRM.
- Campos esperados de campanha, ad group, criativo e teste.
- Evidência de evento/conversão quando houver.
- Regras de first-touch, last-touch e deduplicação.

Se algum input não existir, registre como gap. Não aprove go-live com base em suposição.

## Workflow

1. Extraia os parâmetros esperados da URL:
   - `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`;
   - `v4_client_id`, `v4_campaign_id`, `v4_adgroup_id`, `v4_creative_id`, `v4_test_id`.
2. Submeta ou revise o lead teste.
3. Compare URL vs formulário/campos ocultos.
4. Compare formulário vs planilha backup.
5. Compare planilha backup vs CRM.
6. Verifique:
   - IDs preservados;
   - first-touch não sobrescrito;
   - last-touch atualizado quando aplicável;
   - dedupe funcionando;
   - export permite cruzar lead com campanha/criativo;
   - eventos de conversão foram gerados.
7. Classifique achados:
   - `bloqueador`: impede go-live ou leitura confiável;
   - `alto`: gera risco de falso aprendizado;
   - `medio`: exige correção, mas não bloqueia se risco for aceito;
   - `baixo`: melhoria.
8. Decida: `go`, `go-com-risco`, `no-go` ou `retestar`.

## Output Esperado

Produza:

- checklist de QA;
- comparação esperado vs capturado;
- gaps por camada;
- decisão go/no-go;
- evidências exigidas antes do go-live;
- plano de correção com dono.

Use `templates/checklist-qa-tracking.md` para registro manual.
Use `templates/lead-test-qa.json` com o script para comparar esperado vs capturado.

## Script Utilitário

Para comparar URL esperada, backup e CRM:

```bash
python scripts/compare_tracking_capture.py templates/lead-test-qa.json --md /tmp/qa-tracking.md --csv /tmp/qa-tracking.csv
```

O script ajuda a encontrar divergências, mas a decisão final deve considerar evidências visuais, eventos e contexto operacional.

## Definition Of Done

- URL final contém UTMs e `v4_*`.
- Campos ocultos capturam a origem.
- Planilha backup recebe todos os IDs.
- CRM recebe origem ou há match confiável via backup.
- First-touch e last-touch seguem a regra.
- Lead teste foi registrado com evidência.
- Decisão go/no-go foi documentada.

## Armadilhas

- Validar só a URL e não o CRM.
- Aprovar tracking sem lead teste real.
- Considerar UTM ok mesmo sem `creative_id`.
- Sobrescrever first-touch.
- Não testar dedupe.
- Não verificar se export consegue cruzar lead, campanha e criativo.

## Referências

- Playbook canônico: `assets/canonicos/01_TAXONOMIA_UTM_IDS_E_SUBPARAMETROS.md`
- Detalhamento: `reference.md`
- Template: `templates/checklist-qa-tracking.md`
- Schema: `templates/lead-test-qa.json`
