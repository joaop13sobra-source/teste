# Referência Da Taxonomia UTM E IDs

Fonte normativa: `assets/canonicos/01_TAXONOMIA_UTM_IDS_E_SUBPARAMETROS.md`.

## Princípio

UTM não serve apenas para saber que "veio do Meta". A taxonomia precisa conectar:

```text
investimento -> campanha -> conjunto/ad group -> criativo -> lead -> MQL -> SQL -> oportunidade -> venda
```

Se essa ponte quebra, o time otimiza por CPL e perde qualidade real.

## Convenções

Use sempre:

- letras minúsculas;
- sem acentos;
- sem espaços;
- `-` para separar palavras dentro de um valor;
- `__` para separar blocos/dimensões;
- prefixos curtos;
- valores estáveis.

Regra prática:

```text
nome visível = ID + 3 a 5 dimensões humanas + slug descritivo
análise = IDs + subparâmetros parseados + planilha de growth
```

## IDs Canônicos

| ID | Formato | Exemplo |
| --- | --- | --- |
| Cliente | `cli-{slug_cliente}` | `cli-hs-prevent` |
| Campanha | `cmp-{cliente}-{ano}{mes}-{sequencial}` | `cmp-hs-prevent-202605-001` |
| Ad group/conjunto | `adg-{cliente}-{ano}{mes}-{sequencial}` | `adg-hs-prevent-202605-003` |
| Criativo | `crv-{cliente}-{ano}{mes}-{sequencial}` | `crv-hs-prevent-202605-014` |
| Teste | `tst-{cliente}-{ano}{mes}-{sequencial}` | `tst-hs-prevent-202605-004` |

## Valores Recomendados

### `utm_source`

- `meta`
- `google`
- `linkedin`
- `tiktok`
- `youtube`
- `email`
- `whatsapp`
- `crm`
- `organic`
- `referral`
- `direct`
- `offline`

### `utm_medium`

- `paid_social`
- `paid_search`
- `display`
- `video`
- `organic_social`
- `email`
- `crm`
- `referral`
- `partner`
- `offline`

### Tipo De Campanha

- `aquisicao`
- `remarketing`
- `reativacao`
- `validacao-oferta`
- `captura-demanda`
- `geracao-demanda`
- `conteudo`
- `prova`
- `evento`

### Objetivo

- `leadgen`
- `mql`
- `sql`
- `venda`
- `remarketing`
- `branding`
- `trafego`
- `engajamento`
- `conversao`
- `cadastro`

### Movimento

- `lancamento`
- `always-on`
- `teste-oferta`
- `teste-canal`
- `teste-criativo`
- `escala-vencedor`
- `retomada`
- `prova-social`
- `quebra-crenca`
- `demanda-fria`
- `demanda-quente`

### Formato

- `video`
- `static`
- `carousel`
- `ugc`
- `founder`
- `demo`
- `proof`
- `lp`
- `email`
- `whatsapp`

### Persona

- `cfo`
- `ceo`
- `cto`
- `head-growth`
- `head-produto`
- `gestor-comercial`
- `founder`
- `investidor`
- `comprador-final`

### Hook

- `dor`
- `npa`
- `noticia`
- `beneficio`
- `roi`
- `medo`
- `prova`
- `autoridade`
- `comparativo`
- `diagnostico`
- `urgencia`
- `status`
- `curiosidade`
- `erro-comum`
- `mito`
- `antes-depois`
- `pergunta`
- `oferta-direta`

### Dor

- `fraude`
- `lead-ruim`
- `custo-alto`
- `baixa-conversao`
- `atrito`
- `risco-juridico`
- `tempo-perdido`
- `operacao-manual`
- `falta-contexto`
- `baixa-previsibilidade`

### Ângulo

- `risco-financeiro`
- `perda-oportunidade`
- `comparativo-mercado`
- `antes-depois`
- `autoridade-tecnica`
- `prova-social`
- `demonstracao`
- `educacional`
- `quebra-crenca`
- `oferta-direta`

### Etapa

- `tofu`
- `mofu`
- `bofu`
- `rmkt`
- `reativacao`
- `upsell`

### Temperatura

- `frio`
- `morno`
- `quente`
- `remarketing`
- `lookalike`
- `base`

### Posicionamento

- `interesses`
- `lookalike`
- `lista`
- `retargeting`
- `aberto`
- `keyword`
- `contextual`
- `cargo`
- `empresa`
- `geo`

## Fórmulas De UTM

### `utm_campaign`

```text
{campaign_id}__typ-{tipo_campanha}__obj-{objetivo}__mov-{movimento}__slug-{slug}__coh-{cohort}__seg-{segmento}__per-{periodo}
```

### `utm_content`

```text
{creative_id}__fmt-{formato}__hook-{tipo_hook}__per-{persona}__slug-{slug}__dor-{dor}__ang-{angulo}__stage-{etapa}__ver-{versao}
```

### `utm_term` Social

```text
{adgroup_id}__pub-{publico}__temp-{temperatura}__pos-{posicionamento}__slug-{slug}__plc-{placement}__geo-{geo}
```

### `utm_term` Search

```text
{adgroup_id}__kw-{keyword_slug}__match-{tipo_match}__temp-{temperatura}__slug-{slug}__geo-{geo}
```

## Nomes Visíveis

### Campanha

```text
{campaign_id} | {tipo_campanha} | {objetivo} | {movimento} | {slug}
```

### Ad Group / Conjunto

```text
{adgroup_id} | {publico} | {temperatura} | {posicionamento} | {slug}
```

### Criativo

```text
{creative_id} | {formato} | {hook} | {persona} | {slug} | {versao}
```

## Parâmetros Customizados

Sempre que possível, envie também:

- `v4_client_id`
- `v4_campaign_id`
- `v4_adgroup_id`
- `v4_creative_id`
- `v4_test_id`

## Campos Mínimos Para CRM/Planilha

Identificação:

- `lead_id`
- `created_at`
- `client_id`
- `campaign_id`
- `adgroup_id`
- `creative_id`
- `test_id`

UTMs:

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`
- `utm_term`

Campos parseados:

- `objetivo`
- `tipo_campanha`
- `movimento`
- `campaign_slug`
- `cohort`
- `segmento`
- `periodo`
- `publico`
- `temperatura`
- `posicionamento`
- `adgroup_slug`
- `formato`
- `persona`
- `hook`
- `creative_slug`
- `dor`
- `angulo`
- `etapa_funil`
- `versao`
- `placement`
- `geo`

## Critérios N2/N3

Tracking está N2 quando:

- toda campanha tem ID;
- todo criativo tem ID;
- toda URL tem UTM conforme;
- todo lead carrega origem;
- a fonte da verdade preserva os campos;
- existe teste ponta a ponta registrado.

Tracking está N3 quando:

- a operação usa os campos para decidir;
- performance é agrupada por atributos de criativo;
- qualidade comercial retroalimenta o próximo ciclo;
- aprendizados existem por cohort/segmento;
- o padrão é revisado quando gera ruído ou falso aprendizado.
