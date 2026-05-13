---

name: tracking-audit

description: >

  Advanced tracking setup for paid traffic agencies. Implements Meta CAPI + GA4 + Google Ads using Supabase Edge Functions (server-side), GTM (client-side), and Supabase (data logging). Covers lead gen, e-commerce, and infoproduct scenarios. Captures UTMs, PII, and fires all standard events. Reaches EMQ 9/10 on Meta without Stape, GTM Server-side, or Cloudflare.

description_pt-BR: >

  Implementação de rastreamento avançado para agências de tráfego pago. Configura Meta CAPI + GA4 + Google Ads usando Supabase Edge Functions (server-side), GTM (client-side) e Supabase (log de dados). Cobre cenários de lead gen, e-commerce e infoproduto. Captura UTMs, PII e dispara todos os eventos padrão. Atinge EMQ 9/10 no Meta sem Stape, GTM Server nem Cloudflare. Funciona com qualquer provedor de DNS (Registro.br, GoDaddy, etc.) e qualquer builder (Greatpages, Webflow, WordPress, etc.).

type: hybrid

version: "4.0.0"

categories: [tracking, analytics, ads, gtm, meta, ga4, supabase, capi, utm, ecommerce]

---

# Tracking Avançado — Supabase Edge Function + GTM + Meta CAPI

## Quando usar

Use quando o cliente precisar de rastreamento server-side profissional:
- Meta CAPI com EMQ 8–9/10
- Deduplicação pixel ↔ CAPI via `event_id`
- Captura de UTMs persistida em sessionStorage
- GA4 Measurement Protocol + Google Ads conversions
- Log proprietário no Supabase com todos os dados
- Qualquer tipo de site: lead gen, e-commerce, infoproduto
- Qualquer builder: Greatpages, Webflow, WordPress, Lovable, Wix, Shopify
- Qualquer provedor de DNS: Registro.br, GoDaddy, Cloudflare, etc.

**Sem Cloudflare. Sem Stape. Sem GTM Server. R$ 0/mês.**

---

## Arquitetura geral

```
Browser (qualquer builder com GTM no <head>)
└── GTM Container
    ├── UTM Capture → sessionStorage (All Pages)
    ├── Meta Pixel PageView (client-side)
    ├── GA4 Config (googtag)
    ├── Google Ads Tag (googtag AW-)
    ├── CAPI Edge Function - PageView (server-side)
    ├── Form/Event Listener → push 'lead_captured' ao dataLayer
    │
    └── on 'lead_captured':
        ├── Meta Pixel Lead (Advanced Matching: em,ph,fn,ln + eventID)
        ├── GA4 generate_lead (user_data E.164 + value + currency)
        ├── Google Ads Enhanced Conversion (user_data + gtag conversion)
        └── CAPI Edge Function Lead (email,phone,fn,ln,UTMs,fbp,fbc,event_id)
                    │
                    └── POST → https://{project_ref}.supabase.co/functions/v1/track-event
                        ├── Meta CAPI (server-side, sha256, dedup event_id)
                        ├── GA4 Measurement Protocol
                        └── Supabase log (UTMs + PII + meta_response)
```

**Regra crítica:** usar evento `lead_captured` (não `form_submit`).

Builders como Greatpages e plugins como Elementor/CF7 empurram `form_submit` nativo sem dados PII — nossas tags de conversão só disparam em `lead_captured`, que nosso listener empurra apenas quando todos os campos estão capturados.

---

## Cenários e eventos por tipo de projeto

### 1. Lead Gen (Greatpages, WordPress, Webflow, Lovable)

**Objetivo:** capturar leads via formulário

| Evento | Meta | GA4 | Google Ads | Quando |
|---|---|---|---|---|
| page_view | PageView | page_view | — | Toda página |
| generate_lead | Lead | generate_lead | Conversão Lead | Form submit |

**Campos capturados no form:**
- Nome (split → first_name + last_name)
- Email
- Telefone
- Mensagem (opcional)

**Builders e formulários suportados:**

| Builder / Plugin | Trigger GTM | Seletor nome | Seletor email | Seletor telefone |
|---|---|---|---|---|
| Greatpages (form nativo) | `submit` (form element) | `input[name*="name"], input[placeholder*="nome" i]` | `input[type="email"]` | `input[type="tel"], input[placeholder*="telefone" i]` |
| Elementor Pro | `submit_success` (jQuery) | `input[name="form_fields[name]"]` | `input[name="form_fields[email]"]` | `input[name="form_fields[FIELD_ID]"]` |
| Contact Form 7 | `wpcf7mailsent` (document) | `input[name="your-name"]` | `input[name="your-email"]` | `input[name="your-phone"]` |
| WPForms | `wpformsAjaxSubmitSuccess` | `input[name*="name"]` | `input[type="email"]` | `input[type="tel"]` |
| Gravity Forms | `gform_confirmation_loaded` | `input[id*="input_1"]` | `input[id*="input_2"]` | `input[id*="input_3"]` |
| Typeform (embed) | `message` event (postMessage) | payload `answers[name]` | payload `answers[email]` | payload `answers[phone]` |

---

### 2. E-commerce (WooCommerce / Shopify)

**Objetivo:** rastrear funil completo de compra

| Evento | Meta | GA4 | Google Ads | Quando |
|---|---|---|---|---|
| page_view | PageView | page_view | — | Toda página |
| view_item | ViewContent | view_item | — | Página de produto |
| add_to_cart | AddToCart | add_to_cart | — | Botão "Adicionar" |
| begin_checkout | InitiateCheckout | begin_checkout | — | Início do checkout |
| purchase | Purchase | purchase | Conversão Purchase | Página obrigado / webhook |

**Campos adicionais no Supabase para e-commerce:**

```sql
ADD COLUMN IF NOT EXISTS order_id text,
ADD COLUMN IF NOT EXISTS order_value numeric,
ADD COLUMN IF NOT EXISTS currency text DEFAULT 'BRL',
ADD COLUMN IF NOT EXISTS product_id text,
ADD COLUMN IF NOT EXISTS product_name text;
```

**Payload adicional na Edge Function para Purchase:**

```javascript
{
  event_name: 'purchase',
  event_id: order_id, // usa order_id como event_id (dedup)
  order_id: order_id,
  value: order_value,
  currency: 'BRL',
  email, phone, first_name, last_name,
  utm_source, utm_medium, utm_campaign, ...
}
```

**WooCommerce — captura server-side via webhook:**
- Hook: `woocommerce_payment_complete`
- Enviar POST para `https://{project_ref}.supabase.co/functions/v1/track-event`
- Isso garante Purchase mesmo com ad blocker

**Shopify — captura via Order webhook:**
- Webhook: `orders/paid`
- Registrar em: Shopify Admin → Settings → Notifications → Webhooks

---

### 3. Infoproduto (Hotmart / Kiwify / Eduzz / Monetizze)

**Objetivo:** rastrear visualização da página de vendas + compra via webhook da plataforma

| Evento | Meta | GA4 | Google Ads | Quando |
|---|---|---|---|---|
| page_view | PageView | page_view | — | Toda página |
| view_content | ViewContent | view_item | — | Scroll 50% na página de vendas |
| initiate_checkout | InitiateCheckout | begin_checkout | — | Clique no botão de compra |
| purchase | Purchase | purchase | Conversão Purchase | Webhook da plataforma |

**Webhooks por plataforma:**

| Plataforma | Evento | Campo email | Campo nome | Campo valor |
|---|---|---|---|---|
| Hotmart | `PURCHASE_COMPLETE` | `data.buyer.email` | `data.buyer.name` | `data.purchase.price.value` |
| Kiwify | `order.paid` | `Customer.email` | `Customer.full_name` | `order_value` |
| Eduzz | `transaction_status` (status=3) | `cus_email` | `cus_name` | `trans_value` |
| Monetizze | `postback` (status=3) | `comprador.email` | `comprador.nome` | `valor` |

**Rota adicional na Edge Function para webhooks:**

```javascript
// A Edge Function expõe duas rotas:
// POST /functions/v1/track-event  → eventos do GTM (PageView, Lead)
// POST /functions/v1/track-webhook → webhooks das plataformas (Purchase)
// Mapear campos de cada plataforma para o payload padrão
// Enviar Purchase para Meta CAPI + GA4 + Supabase
```

---

## Dados capturados em TODOS os cenários

### UTMs (captura automática)

Capturados do URL na chegada e persistidos em `sessionStorage`:

```javascript
utm_source | utm_medium | utm_campaign | utm_content | utm_term
```

Enviados em **todos os eventos** (PageView, Lead, Purchase...) — permite rastrear de qual campanha veio cada conversão.

### PII (Lead / Purchase)

| Campo | Normalização | Enviado ao Meta |
|---|---|---|
| email | lowercase + trim | sha256 |
| phone | remove não-dígitos + DDI 55 | sha256 |
| first_name | lowercase + trim | sha256 |
| last_name | lowercase + trim | sha256 |

### Deduplicação

Todo evento de conversão gera um `event_id` único:
- Pixel client-side: `fbq('track', 'Lead', {...}, {eventID: event_id})`
- CAPI server-side: `"event_id": event_id`
- Meta deduplica automaticamente — sem contagem dupla

---

## Supabase Edge Function — deploy

### Estrutura do projeto

```
supabase/
└── functions/
    ├── track-event/
    │   └── index.ts    ← eventos GTM (PageView, Lead)
    └── track-webhook/
        └── index.ts    ← webhooks de plataformas (Purchase)
```

### Deploy via CLI

```bash
# Instalar CLI (uma vez)
npm install -g supabase

# Login
supabase login  # abre browser para autenticar

# Linkar ao projeto
supabase link --project-ref {PROJECT_REF}

# Adicionar secrets (credenciais ficam no ambiente, não no código)
supabase secrets set META_PIXEL_ID={PIXEL_ID}
supabase secrets set META_CAPI_TOKEN={TOKEN}
supabase secrets set GA4_MEASUREMENT_ID={G-XXXXXXXX}
supabase secrets set GA4_API_SECRET={SECRET}
supabase secrets set SUPABASE_SERVICE_ROLE_KEY={KEY}
supabase secrets set TEST_EVENT_CODE={TESTxxxxx}  # remover após validação

# Deploy
supabase functions deploy track-event --no-verify-jwt
supabase functions deploy track-webhook --no-verify-jwt
```

### URL da Edge Function

```
https://{PROJECT_REF}.supabase.co/functions/v1/track-event
https://{PROJECT_REF}.supabase.co/functions/v1/track-webhook
```

Essas URLs são usadas nas tags GTM e configuradas nos webhooks das plataformas.

### Limites do plano gratuito

| Recurso | Gratuito | Suficiente para |
|---|---|---|
| Invocações/mês | 500.000 | ~250.000 leads/mês |
| Funções | Ilimitado | Qualquer quantidade |
| Após limite | $2/milhão | — |

---

## Estrutura da tabela Supabase

Nome: `site_tracking_events_cc_{cliente}` (tudo minúsculo)

```sql
CREATE TABLE IF NOT EXISTS site_tracking_events_cc_{cliente} (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  site text NOT NULL,
  event_name text NOT NULL,
  event_id text,

  -- PII
  email text,
  phone text,
  first_name text,
  last_name text,

  -- UTMs
  utm_source text,
  utm_medium text,
  utm_campaign text,
  utm_content text,
  utm_term text,

  -- Contexto técnico
  page_url text,
  user_agent text,
  ip text,
  fbp text,
  fbc text,
  ga_client_id text,

  -- E-commerce (adicionar se necessário)
  order_id text,
  order_value numeric,
  currency text,

  -- Resposta Meta CAPI
  meta_response jsonb,

  created_at timestamptz DEFAULT now()
);

ALTER TABLE site_tracking_events_cc_{cliente} ENABLE ROW LEVEL SECURITY;
CREATE POLICY service_insert ON site_tracking_events_cc_{cliente}
  FOR INSERT TO service_role WITH CHECK (true);
```

---

## Container GTM — tags geradas

### Tags All Pages

| Tag | Tipo | Função |
|---|---|---|
| UTM - Captura e SessionStorage | html | Lê UTMs do URL, persiste em sessionStorage, push ao dataLayer |
| Meta Pixel - PageView | html | Pixel client-side + fbq PageView |
| GA4 - Config | googtag | Inicializa GA4 |
| Google Ads - Tag | googtag | Inicializa Google Ads |
| Google Ads - Conversao PageView | awct | Conversão de pageview |
| CAPI - Edge Function PageView | html | Envia PageView server-side com UTMs para Supabase Edge Function |
| Form/Event Listener | html | Listener específico por builder/plataforma |

### Tags de Conversão — Setup 10/10

> **Evento exclusivo `lead_captured`** — nunca usar `form_submit` para conversões.
> Builders e plugins empurram `form_submit` nativo sem dados PII.
> Nosso listener empurra `lead_captured` SOMENTE após capturar dados validados.

> **`tagFiringOption` não é suportado no import JSON.** Configurar manualmente
> após importar: Configurações avançadas → Opções de disparo → **Uma vez por página**

| Tag | Tipo | O que inclui |
|---|---|---|
| Meta Pixel - Lead | html | em, ph, fn, ln + value + currency + content_name + eventID |
| GA4 - generate_lead | html | user_data (email, phone E.164, nome) + value + currency |
| Google Ads - Lead Enhanced | html | gtag user_data + conversion + value + currency |
| CAPI - Edge Function Lead | html | email, phone, fn, ln, UTMs, fbp, fbc, event_id → Supabase Edge Function |

**Formatos de telefone por plataforma (crítico):**
- Meta Pixel `ph`: `5516988489132` (sem +, com DDI 55)
- GA4 `phone_number`: `+5516988489132` (E.164 obrigatório com +)
- Google Ads `phone_number`: `+5516988489132` (E.164 obrigatório com +)
- CAPI Edge Function: normalizado server-side antes do sha256

**GA4 generate_lead (estrutura completa):**

```javascript
gtag('event', 'generate_lead', {
  user_data: {
    email_address: email,       // unhashed — GA4 hasheia
    phone_number: '+5516...',   // E.164 com +
    address: { first_name, last_name }
  },
  value: 0, currency: 'BRL'
});
```

**Google Ads Enhanced Conversion (estrutura completa):**

```javascript
gtag('set', 'user_data', {
  email: email,                 // unhashed — Google hasheia
  phone_number: '+5516...',     // E.164 com +
  address: { first_name, last_name }
});
gtag('event', 'conversion', {
  send_to: 'AW-ID/LABEL',
  value: 0, currency: 'BRL'
});
```

> **Pré-requisito Google Ads:** ativar em
> Google Ads → Ferramentas → Conversões → Configurações → Enhanced conversions for web → ON

### Variáveis (13 variáveis)

| Variável | Tipo | Dado |
|---|---|---|
| GA Client ID | Custom JS | Cookie `_ga` |
| Cookie - fbp | 1st party cookie | `_fbp` |
| Cookie - fbc | 1st party cookie | `_fbc` |
| DLV - form_email | Data Layer | `form_email` |
| DLV - form_phone | Data Layer | `form_phone` |
| DLV - form_first_name | Data Layer | `form_first_name` |
| DLV - form_last_name | Data Layer | `form_last_name` |
| DLV - event_id | Data Layer | `event_id` |
| DLV - utm_source | Data Layer | `utm_source` |
| DLV - utm_medium | Data Layer | `utm_medium` |
| DLV - utm_campaign | Data Layer | `utm_campaign` |
| DLV - utm_content | Data Layer | `utm_content` |
| DLV - utm_term | Data Layer | `utm_term` |

---

## EMQ esperado

| Dados | EMQ |
|---|---|
| IP + User Agent | 3–4 |
| + fbp/fbc | 5–6 |
| + Email | 6–7 |
| + Email + Telefone | 7–8 |
| + Email + Telefone + Nome + Sobrenome | **8–9** |
| + fbc presente (vem de anúncio Meta) | **9–9.5** |

---

## Credenciais necessárias

| Dado | Onde encontrar |
|---|---|
| GTM Container ID | tagmanager.google.com |
| Meta Pixel ID | Meta Events Manager |
| Meta CAPI Token | Meta Events Manager → Pixel → Configurações → Conversions API |
| GA4 Measurement ID | GA4 Admin → Fluxos de dados |
| GA4 API Secret | GA4 Admin → Fluxos de dados → Measurement Protocol API Secrets |
| Google Ads Conversion ID | Google Ads → Ferramentas → Conversões |
| Google Ads Labels (por evento) | Um label por tipo de conversão |
| Supabase Project Ref | URL do dashboard Supabase (ex: `abcdefghij`) |
| Supabase Service Role Key | Supabase → Settings → API → service_role |
| Supabase Access Token | Supabase → Account → Access Tokens (`sbp_...`) |

> Cloudflare **não é necessário**. Funciona com qualquer provedor de DNS.

---

## Notas de manutenção

- `test_event_code` (secret `TEST_EVENT_CODE`) deve ser **removido** da Edge Function após validação via `supabase secrets unset TEST_EVENT_CODE`
- CAPI Token USER expira em ~60 dias — migrar para System User Token
- Nome da tabela Supabase é sempre **minúsculo** (PostgreSQL normaliza)
- UTMs persistem em sessionStorage — sobrevivem a navegação interna mas não a nova sessão
- Para e-commerce/infoproduto: webhook da plataforma é obrigatório para capturar Purchase server-side
- Edge Function URL é de terceiro domínio (`supabase.co`) — ad blockers raramente bloqueiam CAPI outbound, mas monitorar no Meta Events Manager
