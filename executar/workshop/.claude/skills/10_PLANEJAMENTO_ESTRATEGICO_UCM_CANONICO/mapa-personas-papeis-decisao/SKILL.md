---
name: mapa-personas-papeis-decisao
description: Mapeia personas e papéis de decisão em B2B, B2C ou alto envolvimento, detalhando dores, desejos, medos, objeções, linguagem, provas, CTA e canais prováveis. Use em UCM, DEOC, planejamento de campanha, copy, LP, mídia, criativos e handoff comercial.
---

# Mapa Personas Papéis Decisão

## Quando Usar

Use quando a comunicação precisa separar quem sofre o problema, quem compra, quem paga, quem bloqueia e quem influencia.

Use especialmente para:

- definir ICP/personas;
- orientar copy e LP;
- separar mensagens por etapa;
- ajustar plano de mídia;
- preparar abordagem comercial;
- mapear comitê de compra.

## Inputs

- discovery;
- CRM;
- feedback de vendas;
- benchmark;
- segmento;
- oferta;
- UCM/DEOC;
- histórico de leads.

## Papéis B2B

- champion/promotor interno;
- decisor econômico;
- blocker técnico;
- usuário final;
- influenciador;
- jurídico/compliance.

## Papéis B2C Ou Alto Envolvimento

- comprador;
- usuário/beneficiário;
- influenciador familiar;
- pagador;
- pessoa que sofre julgamento social.

## Workflow

1. Liste personas relevantes para a compra.
2. Defina o papel de cada uma na decisão.
3. Para cada persona, registre:
   - rotina;
   - dores;
   - desejos;
   - medos;
   - objeções;
   - linguagem;
   - provas que convencem;
   - CTA adequado;
   - canal provável.
4. Identifique conflitos entre papéis.
5. Traduza cada persona para:
   - copy;
   - LP;
   - mídia;
   - criativos;
   - vendas;
   - tracking.

## Output Esperado

- mapa de personas;
- papéis de decisão;
- dores e objeções por papel;
- provas necessárias;
- CTAs e canais prováveis;
- matriz de tradução para ativos.

Use `templates/personas-papeis.md`.
Use `templates/personas-papeis.json` com o script para gerar Markdown/CSV.

## Script Utilitário

```bash
python3 scripts/build_persona_decision_map.py templates/personas-papeis.json --md /tmp/personas.md --csv /tmp/personas.csv
```

## Definition Of Done

- Cada persona tem papel claro na decisão.
- Dores e objeções não são genéricas.
- Há prova associada ao que convence cada papel.
- CTA e canal mudam quando o papel muda.
- Saída orienta campanha e venda.
