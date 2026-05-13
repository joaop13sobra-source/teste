# Referência Do Contrato De Dados Marketing CRM

Fonte normativa: `assets/canonicos/09_CONTRATO_DADOS_MKT_CRM_BACKUP_UTMS_CANONICO.md`.

## Princípio

Tracking só é útil quando permite responder:

```text
qual campanha, conjunto e criativo geraram leads que avançaram no funil?
```

Para isso, a operação precisa de contrato entre mídia, LP/formulário/WhatsApp, planilha backup, CRM, planilha de testes e dashboard/debrief.

## Camadas

### URL

Transporta origem até a LP. Pode se perder se a pessoa navegar ou converter depois.

### Browser/Session Storage/Cookie

Preserva:

- first-touch: gravar uma vez e não sobrescrever;
- last-touch: atualizar a cada visita/conversão relevante.

TTL sugerido: 90 a 180 dias em B2B/inside sales.

### Campos Ocultos

Campos mínimos:

- `first_utm_*`;
- `last_utm_*`;
- `v4_client_id`;
- `v4_campaign_id`;
- `v4_adgroup_id`;
- `v4_creative_id`;
- `v4_test_id`;
- URL da LP;
- timestamp.

### Planilha Backup

Deve existir sempre. Não substitui o CRM; é o cinto de segurança do tracking.

### CRM

Armazena origem, status, avanço comercial, feedback, receita e motivos de perda/desqualificação.

### Base Analítica

Cruza mídia, leads, CRM, UTMs parseadas e qualidade comercial.

## Lead ID

Ideal: UUID gerado no momento da conversão e enviado para planilha backup, CRM, automação, thank-you page e eventos.

Aceitável na v1: hash ou dedupe por email normalizado, telefone normalizado e data.

Evitar: nome, telefone sem normalização ou identificador que muda por sistema.

## Critérios De Qualidade

Bom:

- `unknown_source_rate` menor que 10%;
- `crm_match_rate` maior que 90%;
- `creative_id_fill_rate` maior que 95%;
- `mql_feedback_rate` maior que 80%;
- `lead_id_duplicate_rate` baixo e monitorado.

Alerta:

- mais de 15% de origem desconhecida;
- leads sem `creative_id`;
- CRM sem motivo de desqualificação;
- muitos leads sem primeiro contato;
- backup e CRM divergentes.

## Critério N2

Contrato N2 quando:

- existe planilha backup padronizada;
- UTMs chegam na conversão;
- IDs chegam na planilha;
- CRM recebe origem ou existe match confiável;
- first-touch e last-touch são preservados;
- existe dicionário de dados;
- existe teste ponta a ponta;
- análise pós-campanha é possível.

## Critério N3

Contrato N3 quando:

- dados são atualizados em cadência;
- debrief usa qualidade comercial;
- campanhas são otimizadas por MQL/SQL/venda;
- padrões de criativo são analisados;
- erros de dados viram ação corretiva;
- aprendizados alimentam DEOC/DCC, plano de mídia e briefing.
