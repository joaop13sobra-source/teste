\# Prompt de Início — Rastreamento Avançado v3 

\> Cole este prompt no início de uma nova sessão do Claude Code. 

\--- 

Vou implementar rastreamento avançado completo: \*\*Meta CAPI \+ GA4 \+ Google Ads \+ Supabase \+ UTMs\*\*, usando Cloudflare Worker server-side no mesmo domínio. Sem Stape, sem GTM Server, R$ 0/mês, EMQ 8–9/10. 

Responda as perguntas abaixo de uma vez — o que não souber, me diga e eu oriento. \--- 

\#\# Parte 1 — Tipo de projeto \*(define os eventos e integrações)\* 

\*\*1. Qual é o domínio?\*\* 

\> Ex: \`meusite.com.br\` 

\*\*2. Qual o tipo de projeto?\*\* 

\- \[ \] \*\*Lead Gen\*\* — formulário de contato / agendamento / captura de leads \- \[ \] \*\*E-commerce\*\* — venda de produtos físicos ou digitais direto no site \- \[ \] \*\*Infoproduto\*\* — venda via plataforma externa (Hotmart, Kiwify, Eduzz, Monetizze) \- \[ \] \*\*Misto:\*\* \_\_\_ 

\*\*3. Qual a plataforma do site?\*\* 

\- \[ \] WordPress 

\- \[ \] Lovable / React / Next.js 

\- \[ \] Webflow 

\- \[ \] Wix 

\- \[ \] Shopify 

\- \[ \] Outra: \_\_\_ 

\--- 

\#\# Parte 2 — Formulário / Conversão principal 

\*(responda conforme o tipo de projeto)\* 

\#\#\# Se Lead Gen: 

\*\*4. Qual plugin de formulário?\*\* 

\- \[ \] Elementor Pro 

\- \[ \] Contact Form 7 

\- \[ \] WPForms 

\- \[ \] Gravity Forms 

\- \[ \] Outro: \_\_\_  
\*\*5. Cole o HTML do formulário principal\*\* 

\> F12 no browser → inspecionar o \`\<form\>\` → copiar o HTML 

\> Preciso dos atributos \`name\` ou \`id\` de cada campo (nome, email, telefone) \#\#\# Se E-commerce: 

\*\*4. Qual plataforma de e-commerce?\*\* 

\- \[ \] WooCommerce 

\- \[ \] Shopify 

\- \[ \] Outro: \_\_\_ 

\*\*5. Qual o ticket médio dos produtos?\*\* (para configurar valor de conversão) 

\*\*6. Usa algum gateway de pagamento específico?\*\* 

\> Ex: PagSeguro, Mercado Pago, Pagar.me, Stripe 

\#\#\# Se Infoproduto: 

\*\*4. Qual plataforma?\*\* 

\- \[ \] Hotmart 

\- \[ \] Kiwify 

\- \[ \] Eduzz 

\- \[ \] Monetizze 

\- \[ \] Outro: \_\_\_ 

\*\*5. Qual o produto e valor?\*\* 

\*\*6. O site tem página de vendas própria ou usa a da plataforma?\*\* 

\- \[ \] Página de vendas no meu domínio 

\- \[ \] Página da plataforma (ex: pay.hotmart.com) 

\--- 

\#\# Parte 3 — Cloudflare \*(obrigatório)\* 

\*\*7. O DNS do domínio está no Cloudflare com proxy ativo?\*\* 

\- \[ \] Sim (nuvem laranja no painel Cloudflare) 

\- \[ \] Não — está em outro provedor 

\> ⚠️ O Worker server-side exige Cloudflare com proxy. Se não estiver, usamos Supabase Edge Function como alternativa. 

\*\*8. API Token do Cloudflare\*\* 

\> Criar em: cloudflare.com → My Profile → API Tokens → Create Token → template "Edit Cloudflare Workers" 

\> Me passe o token gerado (começa com \`cfut\_...\` ou similar) 

\---  
\#\# Parte 4 — Meta 

\*\*9. Pixel ID\*\* 

\> 15–16 dígitos. Meta Business → Events Manager 

\*\*10. CAPI Access Token\*\* 

\> Meta Events Manager → Pixel → Configurações → Conversions API → Gerar token \> Token longo começando com \`EAAI...\` 

\*\*11. Código de teste\*\* \*(opcional, para validar em tempo real)\* 

\> Events Manager → Test Events → código \`TESTxxxxx\` 

\--- 

\#\# Parte 5 — Google Analytics 4 

\*\*12. Measurement ID\*\* 

\> Formato: \`G-XXXXXXXXXX\` 

\*\*13. GA4 API Secret\*\* 

\> GA4 → Admin → Fluxos de dados → site → Measurement Protocol API Secrets → Criar \--- 

\#\# Parte 6 — Google Ads \*(se aplicável)\* 

\*\*14. Tem Google Ads ativo?\*\* 

\- \[ \] Sim 

\- \[ \] Não / ainda não 

\*\*15. Conversion ID e Labels por evento\*\* 

\> Google Ads → Ferramentas → Conversões → tag da conversão 

\> Me passe: Conversion ID (número) \+ Label de cada evento que quer rastrear \> Ex: Lead → \`mTIOCI3hzqccEO2j8L4C\` / PageView → \`UHEACJDhzqccEO2j8L4C\` 

\--- 

\#\# Parte 7 — Supabase 

\*\*16. Já tem projeto Supabase?\*\* 

\- \[ \] Sim → me passe: 

\- Project Ref (ID na URL do dashboard) 

\- Service Role Key (Settings → API → service\_role) 

\- Access Token da conta (\`sbp\_...\`) — Account → Access Tokens 

\- \[ \] Não → vou criar junto com você 

\*\*17. Nome/código do cliente para a tabela\*\*  
\> Ex: \`joao\_silva\` → tabela: \`site\_tracking\_events\_cc\_joao\_silva\` 

\--- 

\#\# O que o Claude faz automaticamente 

Com todas as informações acima: 

| Passo | O que faz | 

|---|---| 

| 1 | Cria tabela no Supabase com todas as colunas (PII \+ UTMs \+ eventos) via API | | 2 | Faz deploy do Cloudflare Worker com credenciais como secrets | | 3 | Cria rota \`{dominio}/track/event\` no Cloudflare | 

| 4 | Gera container GTM com todas as tags prontas (1 clique para importar) | | 5 | Testa o Worker e valida no Meta Test Events | 

\*\*Eventos configurados por cenário:\*\* 

\- \*\*Lead Gen:\*\* PageView \+ Lead (com Advanced Matching \+ UTMs) \- \*\*E-commerce:\*\* PageView \+ ViewContent \+ AddToCart \+ InitiateCheckout \+ Purchase \- \*\*Infoproduto:\*\* PageView \+ ViewContent \+ InitiateCheckout \+ Purchase (via webhook) 

\*\*Tempo total:\*\* 30–60 minutos 

\--- 

\*\*Cole todas as respostas acima e começo imediatamente.\*\*