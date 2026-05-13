---
name: contrato-dados-marketing-crm
description: Define contrato de dados entre mídia, LP/formulário, planilha backup, CRM, planilha de testes e dashboard, incluindo UTMs, IDs, first/last-touch, lead_id, match CRM, status de funil e qualidade comercial. Use antes de tracking, backup leads, integração CRM ou análise pós-campanha.
---

# Contrato Dados Marketing CRM

## Quando Usar

Use para garantir que a operação consiga responder quais campanhas, conjuntos e criativos geraram leads que avançaram no funil.

Situações típicas:

- definir dicionário de campos;
- estruturar contrato mídia -> LP -> backup -> CRM;
- preparar análise pós-campanha;
- auditar first/last-touch;
- criar fonte de verdade;
- validar N2 de dados.

## Camadas Do Contrato

1. URL.
2. Browser/session storage/cookie.
3. Campos ocultos no formulário.
4. Planilha backup.
5. CRM.
6. Base analítica/planilha de testes.

## Workflow

1. Liste camadas do fluxo.
2. Defina campos obrigatórios por camada.
3. Defina regras:
   - first-touch write-once;
   - last-touch update on conversion;
   - lead_id único;
   - match CRM;
   - dedupe;
   - status de funil;
   - feedback comercial.
4. Crie dicionário de dados:
   - nome;
   - tipo;
   - descrição;
   - exemplo;
   - obrigatório;
   - fonte;
   - regra de atualização.
5. Verifique critérios N2:
   - backup padronizado;
   - UTMs chegam na conversão;
   - IDs chegam na planilha;
   - CRM recebe origem ou match confiável;
   - first/last-touch preservados;
   - dicionário existe;
   - teste ponta a ponta existe;
   - análise pós-campanha é possível.

## Output Esperado

- contrato de dados;
- dicionário de campos;
- regras first/last-touch;
- regras de match;
- critérios N2/N3;
- gaps de cobertura.

Use `templates/dicionario-dados.md`.
Use `templates/contrato-dados.json` com o script de auditoria.

## Script Utilitário

```bash
python3 scripts/audit_data_contract.py templates/contrato-dados.json --md /tmp/contrato-dados.md --csv /tmp/contrato-dados.csv
```

## Definition Of Done

- Cada campo tem fonte e regra.
- Lead_id está definido.
- First-touch não é sobrescrito.
- Last-touch é atualizado corretamente.
- Backup e CRM preservam origem.
- Análise por campanha/criativo/MQL/SQL é possível.
