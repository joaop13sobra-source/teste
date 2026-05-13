---
name: matriz-problema-proposta-prova
description: Conecta problemas priorizados, impacto, proposta de valor, mecanismo, promessa, objeção, prova e claims pendentes para evitar comunicação sem evidência. Use em UCM, DEOC, DCC, LP, copy, criativos, briefing e revisão estratégica de claims.
---

# Matriz Problema Proposta Prova

## Quando Usar

Use antes de transformar dor em promessa. A skill evita claims soltos, promessa sem prova e copy sem mecanismo.

Use especialmente para:

- priorizar problemas estratégicos;
- criar proposta de valor;
- revisar claims;
- estruturar LP;
- orientar criativos;
- alinhar comercial;
- alimentar DEOC/DCC.

## Inputs

- discovery;
- UCM/DEOC;
- cases;
- números;
- provas;
- objeções;
- restrições jurídicas;
- feedback comercial.

## Workflow

1. Liste problemas reais do público.
2. Para cada problema, registre:
   - descrição objetiva;
   - impacto prático;
   - impacto emocional;
   - impacto financeiro/operacional;
   - voz do cliente;
   - estágio do funil.
3. Conecte cada problema a:
   - proposta de valor;
   - mecanismo;
   - promessa;
   - objeção;
   - prova.
4. Classifique prova:
   - forte;
   - parcial;
   - ausente;
   - proibida/restrita.
5. Marque promessa sem prova como claim pendente.
6. Priorize por impacto, frequência, evidência e risco.

## Output Esperado

- matriz de problemas priorizados;
- proposta de valor por problema;
- mecanismos e promessas;
- provas associadas;
- claims pendentes;
- recomendações para copy, LP, criativo e comercial.

Use `templates/matriz-problema-prova.md`.
Use `templates/matriz-problema-prova.json` com o script para gerar Markdown/CSV.

## Script Utilitário

```bash
python3 scripts/build_problem_proof_matrix.py templates/matriz-problema-prova.json --md /tmp/matriz.md --csv /tmp/matriz.csv
```

## Definition Of Done

- Toda promessa forte tem prova ou vira claim pendente.
- Problema tem impacto e voz do cliente.
- Proposta de valor tem mecanismo.
- Risco jurídico/comercial está marcado.
- Saída orienta ativos executáveis.
