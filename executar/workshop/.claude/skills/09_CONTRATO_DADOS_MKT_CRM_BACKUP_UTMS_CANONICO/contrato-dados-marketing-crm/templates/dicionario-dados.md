# Dicionário De Dados Marketing -> CRM

## Fluxo

- URL:
- Cookie/session:
- Formulário:
- Backup:
- CRM:
- Base analítica:

## Campos

| Campo | Tipo | Fonte | Camada | Obrigatório | Regra de atualização | Exemplo | Descrição |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `lead_id` | string | conversão | backup/CRM | sim | único por lead | `uuid` | Identificador único do lead |
| `first_utm_source` | string | cookie/form | formulário/backup/CRM | sim | write-once | `linkedin` | Primeira fonte conhecida |
| `last_utm_source` | string | cookie/form | formulário/backup/CRM | sim | update on conversion | `google` | Última fonte conhecida |
| `v4_campaign_id` | string | URL/form | formulário/backup/CRM | sim | por conversão | `cmp_cli_2026_05` | ID canônico da campanha |
| `v4_creative_id` | string | URL/form | formulário/backup/CRM | sim | por conversão | `crt_hook_demo_v01` | ID canônico do criativo |
| `is_mql` | boolean | CRM | CRM/base analítica | sim | atualizado no match | `true` | Indica se virou MQL |

## Regras

- First-touch:
- Last-touch:
- Dedupe:
- Match CRM:
- Feedback comercial:
- Fonte da verdade:

## Critérios N2

- [ ] Backup padronizado.
- [ ] UTMs chegam na conversão.
- [ ] IDs chegam na planilha.
- [ ] CRM recebe origem ou match confiável.
- [ ] First-touch preservado.
- [ ] Last-touch preservado.
- [ ] Dicionário existe.
- [ ] Teste ponta a ponta existe.
- [ ] Análise pós-campanha possível.
