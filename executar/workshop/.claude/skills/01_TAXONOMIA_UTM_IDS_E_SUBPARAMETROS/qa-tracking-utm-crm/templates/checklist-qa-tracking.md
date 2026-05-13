# Checklist QA Tracking UTM CRM

## 1. Contexto Do Teste

- Cliente:
- Data:
- Responsável:
- Canal:
- Campanha:
- URL testada:
- Lead teste:
- Decisão: `go` / `go-com-risco` / `no-go` / `retestar`

## 2. URL E Parâmetros Esperados

| Campo | Valor esperado | Encontrado na URL? |
| --- | --- | --- |
| `utm_source` |  |  |
| `utm_medium` |  |  |
| `utm_campaign` |  |  |
| `utm_content` |  |  |
| `utm_term` |  |  |
| `v4_client_id` |  |  |
| `v4_campaign_id` |  |  |
| `v4_adgroup_id` |  |  |
| `v4_creative_id` |  |  |
| `v4_test_id` |  |  |

## 3. Captura No Formulário / Ponto De Conversão

| Campo | Capturado? | Valor | Evidência |
| --- | --- | --- | --- |
| Campos ocultos UTM |  |  |  |
| Campos ocultos `v4_*` |  |  |  |
| Lead ID |  |  |  |
| Timestamp |  |  |  |
| Consentimento/LGPD |  |  |  |

## 4. Planilha Backup

| Campo | Valor esperado | Valor capturado | Status |
| --- | --- | --- | --- |
| `client_id` |  |  |  |
| `campaign_id` |  |  |  |
| `adgroup_id` |  |  |  |
| `creative_id` |  |  |  |
| `test_id` |  |  |  |
| `utm_source` |  |  |  |
| `utm_medium` |  |  |  |
| `utm_campaign` |  |  |  |
| `utm_content` |  |  |  |
| `utm_term` |  |  |  |

## 5. CRM

| Campo | Valor esperado | Valor capturado | Status |
| --- | --- | --- | --- |
| `lead_id` |  |  |  |
| `campaign_id` |  |  |  |
| `adgroup_id` |  |  |  |
| `creative_id` |  |  |  |
| `test_id` |  |  |  |
| `first_utm_*` |  |  |  |
| `last_utm_*` |  |  |  |
| `lead_status` |  |  |  |
| `sales_owner` |  |  |  |

## 6. Regras Críticas

| Regra | Status | Evidência | Observação |
| --- | --- | --- | --- |
| First-touch não sobrescreve |  |  |  |
| Last-touch atualiza quando deve |  |  |  |
| Dedupe funciona |  |  |  |
| Evento de conversão dispara |  |  |  |
| Export permite match |  |  |  |

## 7. Gaps

| Gap | Camada | Severidade | Impacto | Dono | Correção | Reteste necessário |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## 8. Decisão

Decisão final:

Justificativa:

Condições para go-live:

- 
