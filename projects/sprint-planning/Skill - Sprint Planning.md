---

name: sprint-planning

description: >
  Sprint Planning semanal de projetos da V4 Colli&Co. Acessa Ekyte (tarefas/demandas) e grupos de WhatsApp (mensagens do cliente) dos últimos 7 dias, cruza com a análise do gestor e organiza tudo no formato padrão de Sprint Review — com métricas, análise, planos de ação e tasks para subir.

description_pt-BR: >
  Gera o documento de Sprint Planning semanal para um projeto da V4 Colli&Co. Puxa automaticamente as demandas e tarefas do Ekyte, as mensagens recentes do grupo de WhatsApp do cliente, e organiza junto com a análise fornecida pelo usuário no formato padrão de Sprint Review.

type: ops-planning

version: "1.0.0"

categories: [sprint, planning, ekyte, whatsapp, ops, review, tasks]

---

# Sprint Planning — V4 Colli&Co

## Quando usar

Use quando precisar montar o documento de Sprint Planning de um projeto:
- Organizar análise de performance em formato padrão de Sprint Review
- Consolidar demandas do cliente (WhatsApp) e tarefas abertas (Ekyte)
- Gerar lista de ações para subir como tasks no Ekyte
- Fazer projeto a projeto ao longo da semana

---

## Formato de saída padrão (imutável)

```
[Nome do Projeto]
Status do Investimento: R$ X.XXX,XX (XX%)
Leads do mês - XX
MQL - XX
SQL - XX
Vendas - XX
Faturamento Realizado - R$ X.XXX,XX - XX%
Meta Faturamento: R$ XX.XXX,XX
Data da última otimização - DD/MM/AAAA

ANÁLISE
[Texto da análise formatado — CPM, CTR, CPL, taxa de conversão, observações estratégicas]

Planos de ação
1. [Plano de ação 1]
2. [Plano de ação 2]
○ [Sub-item se necessário]

Ações (pra subir task):
[Descrição da task] - DD/MM
[Descrição da task] - DD/MM
```

**Regras de formatação:**
- Nome do projeto sempre entre colchetes como título
- Métricas no cabeçalho: sem linha em branco entre elas
- ANÁLISE: parágrafo corrido, linguagem técnica de tráfego
- Planos de ação: numerados, com sub-itens com ○
- Ações: linha por task com prazo, sem numeração

---

## Fluxo de execução

### PASSO 1 — Identificar o projeto

Perguntar ao usuário: **"Qual projeto vamos montar o sprint planning?"**

Se o usuário não fornecer o nome, pedir antes de prosseguir.

### PASSO 2 — Buscar dados do Ekyte

Usar `ekyte_list_tasks` ou `ekyte_list_tickets` com busca pelo nome do projeto.
Filtrar tarefas criadas ou atualizadas nos **últimos 7 dias**.

Registrar:
- Tarefas em aberto (status != concluído)
- Tarefas concluídas na semana
- Novas solicitações ou tickets

Se o projeto não for encontrado diretamente, usar `ekyte_list_projects` para localizar e depois filtrar tasks por projeto.

### PASSO 3 — Buscar mensagens do WhatsApp

Usar `whatsapp_listar_grupos_queryon` com `search_name` = nome do projeto (ou nome do cliente).

Depois buscar mensagens dos últimos 7 dias com `whatsapp_buscar_mensagens_queryon`:
- `start_date`: 7 dias atrás (YYYY-MM-DD)
- `include_text: true`
- `include_sender_name: true`

Extrair:
- Solicitações explícitas do cliente
- Feedbacks sobre criativos, campanhas, LPs
- Pendências mencionadas
- Aprovações dadas

### PASSO 4 — Solicitar análise ao usuário

Apresentar um resumo do que foi encontrado no Ekyte e WhatsApp, depois pedir:

> "Aqui está o contexto que encontrei. Agora me passa sua análise do projeto (métricas, observações de performance, CPM/CTR/CPL, etc.) que eu monto o Sprint Planning completo."

Se o usuário já passou a análise junto com o comando, pular esta etapa.

### PASSO 5 — Montar o documento

Cruzar tudo e gerar o documento no **formato padrão** (seção acima):
- Métricas: extrair da análise do usuário
- Análise: reescrever/organizar o texto do usuário em parágrafo técnico
- Planos de ação: consolidar intenções do usuário + demandas do WhatsApp
- Ações/tasks: extrair ações concretas com prazos (do Ekyte + do que o usuário mencionar)

---

## Insumos adicionais

Arquivos de contexto extra podem ser colocados em:
```
projects/sprint-planning/insumos/
```

Exemplos de insumos úteis:
- Prints de métricas (CPL, CTR, CPM por campanha)
- Relatórios de período anteriores
- ATAs de reuniões
- Feedbacks específicos do cliente

Ao invocar a skill, informar se há arquivos em insumos que devem ser considerados.

---

## MCPs utilizados

| MCP | Tool | Uso |
|---|---|---|
| `bigquery-whatsapp` | `whatsapp_listar_grupos_queryon` | Localizar grupo do projeto |
| `bigquery-whatsapp` | `whatsapp_buscar_mensagens_queryon` | Puxar mensagens dos últimos 7 dias |
| `ekyte` | `ekyte_list_projects` | Localizar projeto |
| `ekyte` | `ekyte_list_tasks` | Tarefas abertas e da semana |
| `ekyte` | `ekyte_list_tickets` | Tickets/demandas do cliente |

---

## Exemplo de output esperado

```
[Techmax Solar]
Status do Investimento: R$ 5.680,46 (94%)
Leads do mês - 110
MQL - 67
SQL - 47
Vendas - 37
Faturamento Realizado - R$ 205.000,00 - 100%
Meta Faturamento: R$ 200.000,00
Data da última otimização - 08/05/2026

ANÁLISE
CPM estável nas últimas semanas, CTR em 4,27% com taxa de conversão melhorando gradualmente.
Nosso CPL (R$ 51,18) e CPMQL seguem dentro do projetado. Google superou Meta em qualidade —
CPL Google R$ 51,38 vs Meta R$ 64,70. Em maio, CPL do Meta subiu para R$ 88,23 com suspeita de
leads spam, o que demanda atenção imediata no criativo e segmentação.
Perfil do Instagram da Techmax não está sendo indexado pelo Google — possível shadow ban.
Conta profissional confirmada, investigação em andamento.

Planos de ação
1. Investigar e resolver indexação do Instagram no Google
2. Reduzir CPL do Meta em maio abaixo de R$ 70
○ Testar novos criativos com foco em qualificação
○ Revisar segmentação e excluir audiences de baixa qualidade
3. Escalar Google Ads aproveitando menor CPL

Ações (pra subir task):
Verificar shadow ban Instagram Techmax e acionar suporte Meta se necessário - 12/05
Criar variação de criativo Meta com copy focada em qualificação - 14/05
Relatório de performance semanal - 16/05
```

---

## Notas

- Sempre usar a data de hoje como referência para calcular "últimos 7 dias"
- Se não encontrar grupo de WhatsApp, informar e prosseguir só com Ekyte + análise do usuário
- Não inventar métricas — só colocar o que o usuário forneceu explicitamente
- Tasks sem prazo definido: usar prazo padrão de 7 dias a partir de hoje
