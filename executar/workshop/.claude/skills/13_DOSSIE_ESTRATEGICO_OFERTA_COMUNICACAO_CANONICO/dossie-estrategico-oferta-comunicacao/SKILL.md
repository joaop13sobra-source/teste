---
name: dossie-estrategico-oferta-comunicacao
description: Produz ou consolida o Dossiê Estratégico de Oferta e Comunicação (DEOC) como fonte única entre diagnóstico/benchmark e execução, cobrindo resumo estratégico, oferta e mecanismo, ICP/anti-ICP, problemas, alternativas, proposta de valor, narrativa, claims e matriz de tradução para mídia, criativo, LP, vendas e tracking. Use após handoff, diagnóstico GTM, benchmark, TAM/SAM/SOM e beachhead e antes de plano de mídia, briefing criativo, LP, roteiros e scripts comerciais.
---

# Dossiê Estratégico Oferta Comunicação (DEOC)

## Quando Usar

Use quando precisar da **fonte canônica** que substitui a lógica paralela de UCM e DCC: uma narrativa e oferta **auditáveis** que descem até mídia, LP, criativo e vendas sem reinventar promessa.

## Camada De Redação UCM/DCC

Use a referência `executar-ai/workshop/skills/02-documento-comunicacao-ucm-dcc.md` como reforço de redação do DEOC quando o problema for clareza narrativa: ICP/anti-ICP operacional, persona, promessa, provas, objeções, CTA, proposta única de valor e regras de consistência. Não crie um documento paralelo se o DEOC já existe; incorpore esses blocos na seção correspondente do DEOC e registre a mudança no changelog.

## Pré-requisitos (playbook)

**Depois de:** handoff EXECUTAR, diagnóstico GTM, benchmark (mercado, concorrentes, TAM/SAM/SOM), discovery mínimo.

**Antes de:** plano de mídia, briefing criativo, LP, roteiros, campanhas, scripts comerciais.

## Pergunta Que O DEOC Responde

```text
O que vendemos, para quem, por que alguém deveria se importar, contra quais alternativas competimos e como isso vira comunicação executável?
```

## Workflow

1. Colete inputs obrigatórios listados em `reference.md` (Seção 4 do canônico).
2. Preencha na ordem canônica: resumo estratégico → oferta e mecanismo → ICP/personas e anti-ICP → problemas → alternativas → proposta de valor → inimigo/tese/narrativa → claims → tradução para execução.
3. Garanta **oferta dizível**, **escopo explícito**, **provas mínimas** e **limites da promessa**.
4. Codifique as **regras de comunicação**: núcleo que não muda, variações permitidas por canal/cohort e usos em anúncios, LP, vendas e CRM.
5. Separe **claims permitidos**, **proibidos** e **pendentes** (com prova a obter).
6. Valide aderência a N2 com o script de auditoria antes de declarar pronto.
7. Versione mudanças por ciclo quando evoluir para N3 (changelog).

## Outputs

- documento DEOC completo (Markdown ou derivado);
- matriz de tradução para plano de mídia, briefing, LP, copy, vendas e tracking;
- lista de gaps N2 quando o script apontar lacunas.

Use `templates/deoc.md` para redação manual guiada.
Use `templates/deoc.json` com o script para gerar o Markdown estruturado a partir de dados já extraídos.

## Scripts

```bash
python3 scripts/build_deoc.py templates/deoc.json --md /tmp/deoc.md
python3 scripts/build_deoc.py templates/deoc.json --audit
```

## Definition Of Done (N2 mínimo)

O DEOC só conta como N2 se integrar oferta, público, problema, concorrência e narrativa; tiver proposta de valor clara; ICP e anti-ICP operacionais; claims governados; regras de consistência de comunicação; e tradução explícita para execução. Detalhes e checklist em `reference.md` (Seções 6 e 7 do canônico).

Legado: playbooks `04_DCC` e `10_UCM` são contexto de apoio; **fonte operacional** é este DEOC.
