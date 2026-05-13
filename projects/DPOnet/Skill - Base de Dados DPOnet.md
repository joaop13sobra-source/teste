---

name: relatorio-campanhas-gs-engage

description: >
  Relatório de funil comercial da DPOnet via GS Engage API. Puxa leads inbound, MQLs e SQLs de um período, classifica por canal de aquisição (Meta Ads / Google Ads) cruzando com backup CSV do RD Station, e gera tabela consolidada. Cobre também buscas pontuais de leads por email e consulta de dados da Universidade da Privacidade (UP).

description_pt-BR: >
  Relatório de funil comercial da DPOnet via API do GS Engage. Consulta leads de cadências ACTIVE_INBOUND (excluindo DPOday e UP), calcula SQLs (WON com endDate no período) e MQLs (SQLs + LOST com motivos qualificantes), e cruza com backup CSV do RD Station para classificar por canal (Meta Ads / Google Ads / Sem UTM). Também suporta busca de lead por email e relatório separado da UP.

type: data-report

version: "1.0.0"

categories: [crm, gs-engage, leads, funil, sql, mql, meta-ads, google-ads, utm, dponet]

---

# Base de Dados DPOnet — Relatório de Funil por Canal

## Quando usar

Use quando precisar de:
- Volume de leads inbound gerados em um período
- SQLs (oportunidades ganhas) e MQLs do período
- Breakdown por canal de aquisição (Meta Ads vs Google Ads)
- Busca de lead específico por email no GS Engage
- Dados de funil da Universidade da Privacidade (UP)

---

## Regras de negócio (imutáveis)

### Funil padrão DPOnet

| Métrica | Definição |
|---|---|
| **Leads** | Cadências `ACTIVE_INBOUND`, `createdAt` no período, excluindo DPOday e UP |
| **SQL** | Prospection `status=WON` com `endDate` no período |
| **MQL** | SQLs + LOST com motivos qualificantes (ver abaixo) |

### Motivos LOST que entram no MQL

1. Já é cliente / Sendo trabalhado
2. Já entrou outra vez e tem contato com Executivo
3. Não é o momento certo
4. Cliente sendo abordado por parceiro (qualquer variação)

### Classificação de canal

| Canal | Critério |
|---|---|
| **Meta Ads** | `utm_source` ∈ {fb, ig, facebook, instagram, instagram_feed, instagram_stories} **OU** `utm_campaign` contém `[V4]` / `form-nativo` / `criativos` |
| **Google Ads** | `utm_source` ∈ {google, googleads, sitelink} **OU** `utm_medium=cpc` com campaign sem `[V4]` |
| **Sem UTM / Orgânico** | Sem dados UTM identificáveis |

### Cadências excluídas do funil padrão

- DPOday (`acquisitionType` qualquer)
- Universidade da Privacidade — UP (consultada separadamente)

---

## Como executar

### Pré-requisito — API Key

**Sempre solicitar ao usuário a API key do GS Engage antes de qualquer consulta.**
Nunca usar chave hardcoded. Exemplo de prompt:

> "Por favor, me passe a API key do GS Engage para prosseguir."

A API key é passada como query param: `?apiKey={KEY}`

**Base URL:** `https://api.gsengage.com/api/v1`

### Parâmetros de entrada

| Parâmetro | Exemplo | Formato aceito |
|---|---|---|
| Período | "abril 2026" | Por extenso (pt-BR) ou `YYYY-MM` |
| CSV backup | Arquivo .csv do RD Station ou Sheets | Opcional — para cruzamento de UTM |

---

## Passo a passo de execução

### PASSO 1 — Identificar cadências INBOUND

```
GET /routines?apiKey={KEY}&limit=100
```

Filtrar por: `acquisitionType == "ACTIVE_INBOUND"`
Excluir nomes que contenham: `dpoday`, `universidade da privacidade`

### PASSO 2 — Leads do período

```
GET /leads?apiKey={KEY}&routineIds={ids}&orderBy=createdAt&limit=100&page={n}
```

Filtrar: `createdAt` começa com `YYYY-MM` do período.
Email do lead: `lead.emails[0].value`

### PASSO 3 — SQLs (WON)

```
GET /prospections?apiKey={KEY}&status=WON&routineIds={ids}&orderBy=endDate&limit=100&page={n}
```

Filtrar: `endDate` começa com `YYYY-MM` do período.
Lead ID: `prospection.lead.id`

> ⚠️ Alguns SQLs têm `createdAt` fora do período mas `endDate` dentro — incluir todos.
> Para esses, buscar o lead individualmente: `GET /leads/{id}?apiKey={KEY}`

### PASSO 4 — LOST qualificantes (MQL)

```
GET /prospections?apiKey={KEY}&status=LOST&routineIds={ids}&orderBy=endDate&limit=100&page={n}
```

Filtrar: `endDate` no período + `lostReason` contém um dos motivos MQL.

### PASSO 5 — Cruzamento UTM (se CSV disponível)

Para cada email dos leads, buscar no CSV a linha com mais campos UTM preenchidos.
Prioridade: `utm_source` > `utm_campaign` > `utm_medium`

Campos UTM no CSV do Sheets Backup: `utm_source`, `utm_campaign`, `utm_medium`, `utm_content`, `utm_adset`
Campos UTM no CSV do RD Station: `utm source`, `utm medium`, `utm campaign`, `utm_content`

### PASSO 6 — Relatório final

```
RELATÓRIO CANAIS DE AQUISIÇÃO — {PERÍODO}
==========================================

| Canal              | Leads | MQLs | SQLs |
|--------------------|-------|------|------|
| Meta Ads           |   X   |   X  |   X  |
| Google Ads         |   X   |   X  |   X  |
| Sem UTM / Orgânico |   X   |   X  |   X  |
| TOTAL              |   X   |   X  |   X  |
```

---

## Endpoints úteis

| Endpoint | Uso |
|---|---|
| `GET /routines?apiKey={KEY}&limit=100` | Listar cadências |
| `GET /leads?apiKey={KEY}&routineIds={ids}&orderBy=createdAt&limit=100&page={n}` | Leads por cadência |
| `GET /leads/{id}?apiKey={KEY}` | Lead específico por ID |
| `GET /prospections?apiKey={KEY}&status=WON&routineIds={ids}&orderBy=endDate` | SQLs |
| `GET /prospections?apiKey={KEY}&status=LOST&routineIds={ids}&orderBy=endDate` | Perdidos |

**Paginação:** usar `meta.page` e `meta.totalPages` da resposta.
**Rate limit:** incluir `time.sleep(0.2)` entre páginas. Em caso de 429, aguardar 2–3s e tentar novamente.

### Estrutura do objeto lead

```json
{
  "id": "...",
  "fullName": "...",
  "emails": [{ "value": "email@exemplo.com" }],
  "phones": [{ "value": "+5511..." }],
  "companyName": "...",
  "acquisitionType": "ACTIVE_INBOUND",
  "currentRoutineId": "...",
  "createdAt": "2026-04-01T...",
  "customFields": {
    "CNPJ": "...",
    "utm_source": "...",
    "utm_campaign": "...",
    "utm_medium": "...",
    "utm_content": "...",
    "utm_adset": "..."
  }
}
```

### Estrutura do objeto prospection

```json
{
  "id": "...",
  "status": "WON",
  "endDate": "2026-04-15T...",
  "lostReason": null,
  "lead": { "id": "...", "name": "..." }
}
```

---

## Universidade da Privacidade (UP) — consulta separada

Para relatório da UP, usar cadências com nome contendo `universidade da privacidade`:
- `Universidade da Privacidade (UP) - Inbound`
- `Universidade da Privacidade (UP) - Outbound`
- `Universidade da Privacidade (UP) - Feiras e Eventos`

Mesma lógica de SQLs e MQLs, mas sem excluir a UP.

---

## Busca de lead por email

Varrer todas as páginas de `GET /leads?apiKey={KEY}&limit=100&page={n}`.
Comparar `lead.emails[0].value.toLowerCase()` com o email buscado.
Exibir: nome, empresa, CNPJ, telefone, cadência atual, data de criação, UTMs.

> Rate limit: usar `time.sleep(0.2)` por página. Pode levar 30–60s dependendo do volume total de leads.
