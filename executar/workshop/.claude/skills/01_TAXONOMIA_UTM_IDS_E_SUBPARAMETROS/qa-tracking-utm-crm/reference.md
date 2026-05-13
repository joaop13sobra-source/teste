# Referência Do QA Tracking UTM CRM

Fonte normativa: `assets/canonicos/01_TAXONOMIA_UTM_IDS_E_SUBPARAMETROS.md`.

## Objetivo

Garantir que a origem do lead seja preservada desde a URL até a base analítica, permitindo otimizar por MQL, SQL, oportunidade e venda, não apenas por CPL.

## Cadeia De Validação

```text
URL -> browser/cookie/session -> campos ocultos -> planilha backup -> CRM -> planilha de testes/dashboard
```

Cada camada precisa preservar a mesma origem ou registrar uma regra clara de atualização.

## Campos Obrigatórios

### UTMs

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`
- `utm_term`

### IDs `v4_*`

- `v4_client_id`
- `v4_campaign_id`
- `v4_adgroup_id`
- `v4_creative_id`
- `v4_test_id`

### Campos CRM/backup mínimos

- `lead_id`
- `created_at`
- `client_id`
- `campaign_id`
- `adgroup_id`
- `creative_id`
- `test_id`
- `lead_status`
- `mql_status`
- `sql_status`
- `opportunity_status`
- `deal_status`
- `disqualification_reason`
- `sales_owner`
- `first_contact_at`
- `speed_to_lead_minutes`
- `feedback_quality`

## Regras First-Touch E Last-Touch

First-touch:

- gravar uma vez;
- não sobrescrever em nova visita;
- preservar primeira origem relevante;
- conter `first_utm_source`, `first_utm_medium`, `first_utm_campaign`, `first_utm_content`, `first_utm_term`, `first_conversion_at`.

Last-touch:

- atualizar em nova conversão relevante;
- registrar última origem antes da conversão;
- conter `last_utm_source`, `last_utm_medium`, `last_utm_campaign`, `last_utm_content`, `last_utm_term`, `last_conversion_at`.

## Teste Obrigatório Antes Do Go-Live

Checklist mínimo:

1. Abrir URL com UTMs.
2. Confirmar que a LP carrega sem perder query string.
3. Submeter formulário teste.
4. Validar campos ocultos.
5. Verificar planilha backup.
6. Verificar CRM.
7. Verificar evento de conversão.
8. Verificar IDs preservados.
9. Verificar first-touch.
10. Verificar last-touch.
11. Verificar dedupe.
12. Verificar export para análise.

## Decisão Go/No-Go

### `go`

Use quando:

- todos os campos obrigatórios chegaram;
- CRM ou backup permite match confiável;
- first-touch/last-touch funcionam;
- lead teste e evidências estão registrados.

### `go-com-risco`

Use quando:

- há gap não bloqueador;
- o risco foi explicitamente aceito;
- existe plano corretivo e dono;
- análise mínima continua possível.

### `no-go`

Use quando:

- campanha, criativo ou lead não preserva ID;
- CRM/backup não recebe origem;
- first-touch sobrescreve;
- não há lead teste;
- export não permite cruzar lead com campanha/criativo;
- evento principal não foi validado.

### `retestar`

Use quando:

- correção foi feita;
- evidência é inconclusiva;
- teste foi executado em ambiente errado;
- dados chegaram atrasados ou duplicados.

## Severidade

- `bloqueador`: impede go-live, match ou leitura confiável.
- `alto`: pode gerar falso aprendizado ou perda relevante de origem.
- `medio`: afeta completude, mas pode ser aceito temporariamente.
- `baixo`: melhoria de governança ou padronização.

## Falsos Positivos Comuns

- A plataforma mostra lead, mas CRM não tem origem.
- A URL tem UTM, mas campos ocultos não capturam.
- A planilha recebe `utm_source`, mas não recebe `creative_id`.
- First-touch funciona em uma visita, mas é sobrescrito em retorno.
- Last-touch nunca atualiza.
- Dedupe junta leads diferentes por telefone incompleto.
- Export de CRM não contém campos necessários para análise.

## Critério N2

Tracking está N2 quando:

- toda campanha tem ID;
- todo criativo tem ID;
- toda URL tem UTM conforme;
- todo lead carrega origem;
- fonte da verdade preserva os campos;
- existe teste ponta a ponta registrado.

## Critério N3

Tracking está N3 quando:

- campos são usados para decisão;
- performance é agrupada por atributos de criativo;
- qualidade comercial retroalimenta o próximo ciclo;
- aprendizados existem por cohort/segmento;
- padrão é revisado quando gera ruído ou falso aprendizado.
