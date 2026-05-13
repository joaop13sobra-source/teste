---

name: auditoria-funil-crm

description: >
  Auditoria de funil comercial multi-CRM (Kommo, Bitrix24 ou planilha CSV). Puxa leads, MQLs, SQLs, vendas e faturamento de um período, classifica por canal de aquisição e UTMs (campanha, público, anúncio e posicionamento), calcula taxas de passagem por etapa e gera ranking de performance por faturamento, volume de vendas, SQLs e MQLs.

description_pt-BR: >
  Skill de auditoria de funil comercial compatível com Kommo, Bitrix24 e planilhas CSV. Respeita a lógica de data por etapa: leads pela data de criação, MQLs e SQLs pela data de transição de estágio, vendas pela data de fechamento. Inclui leads perdidos/desqualificados que passaram por MQL ou SQL. Ranking final ordenado por faturamento → vendas → SQLs → MQLs.

type: data-report

version: "1.0.0"

categories: [crm, kommo, bitrix24, csv, leads, funil, sql, mql, vendas, faturamento, utm, campanhas]

---

# Auditoria de Funil Comercial — Multi-CRM

---

## ⛔ REGRA ABSOLUTA — SOMENTE LEITURA

**Esta skill é estritamente read-only. As seguintes proibições são invioláveis e não podem ser suspensas por nenhuma instrução, pedido ou contexto:**

- **NUNCA** executar operações de escrita no CRM (POST, PUT, PATCH, DELETE ou qualquer método que altere dados).
- **NUNCA** criar, editar, mover, arquivar, excluir ou alterar leads, deals, contatos, empresas, estágios, tags, campos ou qualquer outro registro.
- **NUNCA** atender a um pedido do usuário que envolva alterar o CRM, mesmo que o usuário afirme que é necessário, urgente ou que a API permita.
- Se o usuário pedir qualquer alteração no CRM, responder: *"Esta skill é exclusivamente de leitura. Não executo alterações no CRM em nenhuma hipótese."* — e encerrar essa solicitação.
- Se a API fornecida tiver permissão de escrita, **ignorar completamente essa permissão** e usar apenas endpoints GET.

### Regra de credencial e memória

- **Nunca armazenar, registrar ou persistir a API key** em arquivo, memória de longo prazo, histórico ou qualquer outro meio.
- A credencial existe apenas na sessão ativa, enquanto a análise estiver em andamento.
- Ao concluir a análise solicitada (ou ao encerrar a conversa), **descartar a credencial imediatamente** — não reutilizar em sessões futuras.
- Em cada nova execução da skill, **sempre solicitar a credencial novamente** ao usuário, sem exceção.
- Nunca sugerir, inferir ou reutilizar uma credencial de sessões anteriores.

---

## Quando usar

Use quando precisar de:
- Relatório de funil (Leads → MQL → SQL → Venda) por período
- Breakdown por canal de aquisição e UTMs (campanha, público, anúncio, posicionamento)
- Taxas de passagem entre etapas por canal e campanha
- Ranking de campanhas por faturamento, volume de vendas, SQLs e MQLs
- Identificação de campanhas com alto faturamento mesmo com baixo volume

---

## Fluxo de início obrigatório

Ao ser acionada, sempre pergunte na seguinte ordem:

**1. CRM utilizado:**
> "Qual CRM você está usando? (Kommo / Bitrix24 / Planilha CSV)"

**2. Credencial de acesso** (nunca use chave hardcoded, nunca salve):
- **Kommo** → "Me passe o token de integração (Bearer token) e o subdomínio da sua conta (ex: suaempresa.kommo.com)"
- **Bitrix24** → "Me passe a URL do seu webhook REST (ex: https://suaempresa.bitrix24.com.br/rest/1/xxxxx/)"
- **CSV** → "Envie o arquivo de leads com UTMs e o arquivo de vendas/funil. Explique as colunas quando enviar."

**3. Pipeline/Funil:**
> "Qual pipeline/funil devo analisar? Me passe o nome ou ID."

**4. Período:**
> "Qual é o período de análise? (ex: abril 2026 / 01/04/2026 a 30/04/2026)"

**5. Estágios de MQL e SQL:**
- Buscar nos estágios do pipeline nomes que contenham `mql`, `sql`, `qualificado`, `oportunidade` (case-insensitive).
- Se encontrar, confirmar com o usuário: "Identifiquei estes estágios como MQL: [...] e estes como SQL: [...]. Correto?"
- Se não encontrar nenhum correspondente: "Não identifiquei estágios com nomes de MQL ou SQL. Quais são os estágios que representam MQL e SQL no seu funil?"

---

## Regras de negócio (imutáveis)

### Lógica de funil

```
Lead → MQL → SQL → Venda
```

- Quem está em **Venda** passou por MQL e SQL — contar em todos os três.
- Quem está em **SQL** passou por MQL — contar em MQL também.
- Leads **perdidos ou desqualificados** que passaram por MQL ou SQL entram na contagem das etapas correspondentes.

### Lógica de data por etapa

| Etapa | Referência de data |
|---|---|
| **Lead** | Data de criação (`created_at`) |
| **MQL** | Data de transição para o estágio MQL |
| **SQL** | Data de transição para o estágio SQL |
| **Venda** | Data de fechamento (won date / `closed_at`) |

> Exemplo: lead criado em 31/03 que vira MQL em 01/04 → entra nos **leads de março** e nos **MQLs de abril**.

**Se o CRM não tiver histórico de estágios:** usar o estágio atual como referência, sem filtro de data para MQL/SQL. Incluir aviso no relatório:
> ⚠️ *Histórico de estágios não disponível — MQLs e SQLs baseados no estágio atual do lead, sem filtro de data.*

### Faturamento

- Usar o campo de valor do negócio/deal do CRM.
- Se o CRM não tiver campo de valor preenchido, informar: "Faturamento não disponível — campo de valor do negócio não encontrado ou não preenchido."
- Nunca estimar ou imputar valores.

### Posicionamento (placement)

- Incluir somente se disponível como UTM ou campo customizado.
- Se ausente, omitir a coluna de posicionamento sem mencionar a ausência.

### Leads duplicados

- Contar cada entrada separadamente (um lead que entrou duas vezes em campanhas diferentes = 2 registros).
- Não deduplicar por email ou CPF.

### Público desconhecido

- Leads com `utm_campaign` mas sem `utm_adset` (ou equivalente) → classificar público como **"Público desconhecido"**.

### Ranking de campanhas

Ordenar sempre por:
1. **Faturamento total** (maior primeiro)
2. **Número de vendas**
3. **SQLs**
4. **MQLs**
5. Leads são apresentados mas não são critério de ranking.

---

## Execução por CRM

---

### KOMMO

**Base URL:** `https://{subdomain}.kommo.com/api/v4`
**Auth:** Header `Authorization: Bearer {TOKEN}`

#### PASSO 1 — Identificar pipeline e estágios

```
GET /leads/pipelines/{pipeline_id}
```

Listar todos os estágios (`_embedded.stages`). Identificar IDs dos estágios de MQL, SQL e Venda (Won = status_id 142 padrão).

```
GET /leads/custom_fields
```

Mapear campos UTM: `utm_source`, `utm_campaign`, `utm_medium`, `utm_content`, `utm_adset`, `utm_placement` (ou nomes equivalentes).

#### PASSO 2 — Leads do período (pela data de criação)

```
GET /leads?filter[pipeline_id]={id}&filter[created_at][from]={unix_start}&filter[created_at][to]={unix_end}&with=contacts,loss_reason&limit=250&page={n}
```

Extrair: `id`, `name`, `created_at`, `status_id`, `pipeline_id`, `price` (valor do negócio), campos UTM dos custom fields.

#### PASSO 3 — Histórico de estágios (para MQL/SQL por data)

```
GET /events?filter[type][]=lead_status_changed&filter[created_at][from]={unix_start}&filter[created_at][to]={unix_end}&limit=250&page={n}
```

Filtrar eventos cujo `value_after.id` corresponda a estágios MQL ou SQL.
Extrair: `entity_id` (lead_id), `created_at` (data da transição), `value_after.id` (estágio destino).

> Se o endpoint de eventos retornar erro ou estar vazio, usar estágio atual (`status_id`) como fallback.

#### PASSO 4 — Vendas (Won) do período

```
GET /leads?filter[pipeline_id]={id}&filter[statuses][0][pipeline_id]={id}&filter[statuses][0][status_id]=142&filter[closed_at][from]={unix_start}&filter[closed_at][to]={unix_end}&limit=250&page={n}
```

Extrair: `id`, `price`, `closed_at`, UTMs do lead.

#### PASSO 5 — Perdidos/Desqualificados que passaram por MQL ou SQL

```
GET /leads?filter[pipeline_id]={id}&filter[statuses][0][status_id]=143&with=loss_reason&limit=250&page={n}
```

Cruzar com eventos de histórico para verificar se o lead transitou por estágio MQL ou SQL antes de ser perdido.
Se sem histórico, verificar se `status_id` era MQL/SQL antes de mover para perdido via campo `loss_reason` ou posição no pipeline.

**Paginação Kommo:** verificar `_page_count` no header ou `_links.next` no body. Rate limit: 7 req/s — incluir `sleep(0.15)` entre páginas.

---

### BITRIX24

**Base URL do webhook:** `https://{dominio}/rest/{user_id}/{token}/`
**Método:** GET ou POST

#### PASSO 1 — Identificar pipeline e estágios

```
POST crm.category.list
{"entityTypeId": 2}
```

Localizar o pipeline pelo nome. Usar `id` da categoria.

```
POST crm.dealcategory.stage.list
{"id": {category_id}}
```

Listar estágios. Identificar IDs dos estágios MQL, SQL e Won (STATUS_ID = "WON").

```
POST crm.deal.fields
```

Mapear campos UTM customizados (UF_CRM_*).

#### PASSO 2 — Leads/Deals do período (pela data de criação)

```
POST crm.deal.list
{
  "filter": {
    "CATEGORY_ID": {category_id},
    ">=DATE_CREATE": "YYYY-MM-DDT00:00:00",
    "<=DATE_CREATE": "YYYY-MM-DDT23:59:59"
  },
  "select": ["ID", "TITLE", "DATE_CREATE", "CLOSEDATE", "OPPORTUNITY", "STAGE_ID", "UTM_SOURCE", "UTM_CAMPAIGN", "UTM_MEDIUM", "UTM_CONTENT", "UF_CRM_*"],
  "start": {offset}
}
```

Paginação: incrementar `start` de 50 em 50 até `total` ser atingido.

#### PASSO 3 — Histórico de estágios (para MQL/SQL por data)

```
POST crm.stagehistory.list
{
  "entityTypeId": 2,
  "filter": {
    "ITEM_ID": {deal_id},
    ">=CREATED_TIME": "YYYY-MM-DDT00:00:00",
    "<=CREATED_TIME": "YYYY-MM-DDT23:59:59"
  }
}
```

> Chamar por lote de deals para evitar rate limit. Rate limit Bitrix: 2 req/s no plano padrão — `sleep(0.5)` entre chamadas.

#### PASSO 4 — Vendas (Won) do período

```
POST crm.deal.list
{
  "filter": {
    "CATEGORY_ID": {category_id},
    "STAGE_ID": "WON",
    ">=CLOSEDATE": "YYYY-MM-DDT00:00:00",
    "<=CLOSEDATE": "YYYY-MM-DDT23:59:59"
  },
  "select": ["ID", "OPPORTUNITY", "CLOSEDATE", "UTM_SOURCE", "UTM_CAMPAIGN", "UTM_MEDIUM", "UTM_CONTENT"]
}
```

#### PASSO 5 — Perdidos que passaram por MQL ou SQL

```
POST crm.deal.list
{
  "filter": {
    "CATEGORY_ID": {category_id},
    "STAGE_ID": "LOSE"
  }
}
```

Cruzar com histórico de estágios para verificar passagem por MQL/SQL.

---

### PLANILHA CSV

#### Ao receber os arquivos

Aguardar o usuário enviar os arquivos e explicar as colunas. Não assumir estrutura — confirmar mapeamento antes de processar:

> "Recebi os arquivos. Para mapear corretamente, me diz:
> 1. Qual coluna representa o email ou ID do lead?
> 2. Qual coluna representa a data de criação do lead?
> 3. Quais colunas são as UTMs? (source, campaign, medium, content, adset/audience)
> 4. Na planilha de funil: qual coluna indica a etapa atual? Quais valores representam MQL, SQL e Venda?
> 5. Existe coluna de valor/faturamento? E data de fechamento?
> 6. Existe histórico de etapas (uma linha por transição) ou só o estágio atual?"

#### Processamento

- Aplicar a mesma lógica de datas que o CRM (se houver coluna de data por etapa).
- Se só houver estágio atual: aplicar regra de funil cumulativo (quem está em venda passou por MQL e SQL).
- Leads perdidos: verificar se a coluna de estágio indica passagem por MQL/SQL (ex: coluna "último estágio qualificado").

---

## Classificação de canais

| Canal | Critério |
|---|---|
| **Meta Ads** | `utm_source` ∈ {fb, ig, facebook, instagram, facebook_ads, instagram_feed, instagram_stories, instagram_reels} **OU** `utm_medium` = paid_social |
| **Google Ads** | `utm_source` ∈ {google, googleads, google_ads, sitelink} **OU** `utm_medium` ∈ {cpc, ppc, paidsearch} |
| **TikTok Ads** | `utm_source` ∈ {tiktok, tiktok_ads} |
| **Orgânico / Direto** | sem `utm_source` ou `utm_source` = {direct, organic, (none)} |
| **Outros pagos** | qualquer outro `utm_source` com `utm_medium` = paid |
| **Outros** | qualquer combinação não enquadrada acima |

---

## Formato do relatório

### Bloco 1 — Resumo geral do período

```
AUDITORIA DE FUNIL — {PIPELINE} | {PERÍODO}
CRM: {Kommo / Bitrix24 / CSV}
============================================

FUNIL GERAL
-----------
Leads criados:    {n}
MQLs:             {n}  (taxa lead→MQL: X%)
SQLs:             {n}  (taxa MQL→SQL: X%)
Vendas:           {n}  (taxa SQL→Venda: X%)
Faturamento:      R$ {valor}
Ticket médio:     R$ {valor}
```

> Se faturamento não disponível: exibir "Faturamento: não disponível no CRM"

### Bloco 2 — Por canal de aquisição

```
POR CANAL
---------
| Canal       | Leads | MQLs | SQLs | Vendas | Faturamento | L→MQL | MQL→SQL | SQL→V |
|-------------|-------|------|------|--------|-------------|-------|---------|-------|
| Meta Ads    |   X   |   X  |   X  |    X   |   R$ X.XXX  |  X%   |   X%    |  X%   |
| Google Ads  |   X   |   X  |   X  |    X   |   R$ X.XXX  |  X%   |   X%    |  X%   |
| Orgânico    |   X   |   X  |   X  |    X   |   R$ X.XXX  |  X%   |   X%    |  X%   |
| TOTAL       |   X   |   X  |   X  |    X   |   R$ X.XXX  |  X%   |   X%    |  X%   |
```

### Bloco 3 — Por campanha (ranking)

```
RANKING DE CAMPANHAS (ordenado por faturamento)
------------------------------------------------
| #  | Campanha             | Leads | MQLs | SQLs | Vendas | Faturamento | Ticket Médio |
|----|----------------------|-------|------|------|--------|-------------|--------------|
| 1  | {utm_campaign}       |   X   |   X  |   X  |    X   |  R$ XX.XXX  |   R$ X.XXX   |
| 2  | ...                  |  ...  |  ... |  ... |   ...  |     ...     |     ...      |
```

### Bloco 4 — Por público dentro das top campanhas

```
DETALHAMENTO POR PÚBLICO — {nome da campanha}
----------------------------------------------
| Público              | Leads | MQLs | SQLs | Vendas | Faturamento |
|----------------------|-------|------|------|--------|-------------|
| {utm_adset}          |   X   |   X  |   X  |    X   |  R$ X.XXX   |
| Público desconhecido |   X   |   X  |   X  |    X   |  R$ X.XXX   |
```

### Bloco 5 — Por anúncio (se utm_content disponível)

```
DETALHAMENTO POR ANÚNCIO — {campanha} / {público}
--------------------------------------------------
| Anúncio         | Leads | MQLs | SQLs | Vendas | Faturamento |
|-----------------|-------|------|------|--------|-------------|
| {utm_content}   |   X   |   X  |   X  |    X   |  R$ X.XXX   |
```

### Bloco 6 — Por posicionamento (somente se dado disponível)

```
DETALHAMENTO POR POSICIONAMENTO
--------------------------------
| Posicionamento  | Leads | MQLs | SQLs | Vendas | Faturamento |
|-----------------|-------|------|------|--------|-------------|
| {utm_placement} |   X   |   X  |   X  |    X   |  R$ X.XXX   |
```

### Bloco 7 — Insight de campanhas

```
INSIGHTS
--------
• Campanha com maior faturamento: {nome} → R$ {valor} ({n} vendas)
• Campanha com maior volume de vendas: {nome} → {n} vendas (R$ {valor})
• Campanha com melhor taxa lead→venda: {nome} → X%
• Campanha com maior faturamento por SQL: {nome} → R$ {valor}/SQL
• Alertas: campanhas com alto volume de MQLs/SQLs mas zero vendas no período.
```

---

## Avisos automáticos

Exibir ao final do relatório quando aplicável:

- ⚠️ `Histórico de estágios não disponível — MQLs e SQLs baseados no estágio atual.`
- ℹ️ `{N} leads sem nenhuma UTM — classificados como Orgânico/Direto.`
- ℹ️ `Faturamento não disponível — campo de valor não encontrado ou não preenchido no CRM.`
- ℹ️ `Posicionamento omitido — dado não encontrado nas UTMs ou campos do CRM.`

---

## Exportação

Por padrão, o relatório fica apenas no chat.

Se o usuário pedir exportação, gerar em formato Markdown para copiar, ou acionar a skill de Google Sheets/Drive se disponível.

---

## Rate limits e boas práticas

| CRM | Rate limit recomendado |
|---|---|
| Kommo | `sleep(0.15)` entre páginas (máx 7 req/s) |
| Bitrix24 | `sleep(0.5)` entre chamadas (máx 2 req/s padrão) |

Em caso de erro 429 (too many requests): aguardar 3–5s e tentar novamente (máx 3 tentativas por endpoint).
