---
name: iterador-skills-marketing-os
description: Atualiza, melhora, ajusta ou estende skills do Marketing OS com base no workflow mais recente, no playbook canonico acima da skill e nas boas praticas de criacao de skills. Use quando o usuario pedir revisao, iteracao, melhoria, extensao, refatoracao, alinhamento canonico ou criacao derivada de skills em workflow_marketing_os_v1/.claude/skills.
---

# Iterador Skills Marketing OS

## Quando Usar

Use quando precisar mexer em skills existentes ou criar uma skill derivada dentro do Marketing OS.

Casos tipicos:

- melhorar uma skill sem perder o contrato do playbook canonico;
- ajustar `SKILL.md`, `reference.md`, templates ou scripts de uma skill;
- estender uma skill para cobrir uma nova capacidade operacional;
- revisar se uma skill esta pequena, invocavel, orientada a output e auditavel;
- sincronizar skills depois de mudanca no workflow, nos canonicos ou nos indices;
- avaliar varias skills de um playbook antes de editar.

Nao use para:

- reescrever playbooks canonicos;
- editar todas as 70+ skills sem escopo claro;
- transformar playbook inteiro em uma skill gigante;
- alterar o workflow visual quando a mudanca e apenas interna de skill.

## Fontes Obrigatorias

Antes de editar qualquer skill, contextualize nesta ordem:

1. Workflow mais recente: `workflow.knowledge-os.vN.json`, usando o maior `N` existente, salvo se o usuario especificar versao.
2. Mapa de skills: `playbook-skills.json` e, se existir gerado, `skills-index.json`.
3. Skill alvo: `SKILL.md` e arquivos auxiliares relevantes no mesmo diretorio.
4. Playbook canonico acima da skill: para `.claude/skills/<PLAYBOOK_DIR>/<skill>/SKILL.md`, leia `assets/canonicos/<PLAYBOOK_DIR>.md`.
5. Para skills transversais, leia tambem `assets/canonicos/00_MAPA_ASSETS_AI_NATIVE_PONTA_A_PONTA.md` e os canonicos dos playbooks afetados.
6. Boas praticas em `metodologia-criacao-skills/01_REFERENCIA_CLAUDE_CODE_SKILLS.md`, quando a mudanca envolver estrutura de skill.

Use o script de contexto para descobrir os caminhos:

```bash
python3 .claude/skills/00_MAPA_ASSETS_AI_NATIVE_PONTA_A_PONTA/iterador-skills-marketing-os/scripts/contextualizar_skill.py --skill <skill-id-ou-caminho>
```

Para auditar um playbook inteiro:

```bash
python3 .claude/skills/00_MAPA_ASSETS_AI_NATIVE_PONTA_A_PONTA/iterador-skills-marketing-os/scripts/contextualizar_skill.py --playbook <PLAYBOOK_DIR>
```

## Workflow De Iteracao

1. Defina o escopo: uma skill, varias skills de um playbook, ou uma nova skill.
2. Rode o script de contexto e confirme:
   - workflow mais recente;
   - playbook canonico correspondente;
   - skills irmas no mesmo playbook;
   - arquivos auxiliares existentes.
3. Leia somente o necessario do workflow:
   - `canonicalDocuments`;
   - macros/assets que citam o `docPath`;
   - `iterationNotes`;
   - dependencias ou outputs relacionados.
4. Leia o playbook canonico acima da skill para entender contrato, vocabulario, DoD, N2/N3, entradas e saidas.
5. Leia a skill atual e classifique o tipo de mudanca:
   - `melhoria`: clareza, gatilho, DoD, output, fronteiras;
   - `ajuste`: bug, ambiguidade, referencia quebrada, script/template;
   - `extensao`: nova capacidade dentro da mesma fronteira;
   - `nova skill`: capacidade independente que merece pasta propria.
6. Planeje a edicao minima: o que muda em `SKILL.md`, o que deve ir para `reference.md`, template ou script, e o que nao sera tocado.
7. Edite preservando o papel da skill:
   - mantenha o frontmatter claro e acionavel;
   - nao copie o playbook inteiro;
   - mova detalhes longos para `reference.md`;
   - mantenha workflow, inputs, outputs e Definition of Done auditaveis;
   - cite dependencias para outras skills quando isso evitar duplicacao;
   - preserve nomes e caminhos salvo decisao explicita.
8. Atualize indices e valide.

## Criterios De Qualidade

Uma iteracao boa deixa a skill:

- pequena o suficiente para ser carregada sem poluir contexto;
- especifica o suficiente para disparar no momento certo;
- conectada ao playbook canonico certo;
- orientada a outputs concretos;
- com inputs minimos e DoD verificavel;
- com fronteiras claras de quando nao usar;
- sem duplicar conteudo normativo longo;
- capaz de empurrar gaps para backlog, QA ou skill especialista quando necessario.

Use `reference.md` para a rubrica completa.

## Validacao

Depois de mexer em qualquer skill:

```bash
node build-docs.mjs
python3 -m json.tool workflow.manifest.json > /tmp/workflow-manifest-check.json
python3 -m json.tool workflow.knowledge-os.v3.json > /tmp/workflow-latest-check.json
```

Se existir `workflow.knowledge-os.v4.json` ou superior, valide a versao mais recente no lugar de `v3`.

Quando scripts forem alterados, rode `python3 -m py_compile <script.py>` ou o comando de teste do proprio script.

## Output Esperado

Ao finalizar, entregue:

- skills alteradas ou criadas;
- arquivos auxiliares alterados;
- fonte canonica usada;
- validacoes executadas;
- pendencias ou riscos restantes.

## Referencias

- Playbook canonico transversal: `assets/canonicos/00_MAPA_ASSETS_AI_NATIVE_PONTA_A_PONTA.md`
- Rubrica: `reference.md`
- Plano de iteracao: `templates/plano-iteracao-skill.md`
- Script de contexto: `scripts/contextualizar_skill.py`
